"""Async HTTP request objects built on top of ``httpx``."""

import asyncio
import random
import urllib.parse

import httpx

from crawley import config


async def _capped_stream(client, method, url, headers, data=None):
    """Stream a request and stop reading past ``config.MAX_RESPONSE_BYTES``.

    A plain ``client.get`` / ``client.post`` buffers the whole body into RAM, so
    one huge or mislabeled response (a media file / tarball caught by a link
    follow) can OOM-kill the process. This streams and hard-stops mid-body, then
    buffers the capped bytes back onto the SAME response object (``_content`` —
    exactly what ``Response.read()`` does) so ``.text`` / ``.headers`` / ``.url``
    / history / cookies are all preserved. Uses ``client.stream()`` so redirects,
    the SSRF request hook and connection-pool release work exactly like the
    buffered call.

    An oversized body is **truncated** to the first ``MAX_RESPONSE_BYTES`` — never
    discarded — so the extractor still sees the leading (usable) HTML rather than
    an empty page. We do not trust ``Content-Length`` to short-circuit: it is the
    wire size (possibly gzip'd, or simply wrong), so streaming-and-truncating on
    the decoded bytes is the only correct measure.
    """
    max_bytes = getattr(config, "MAX_RESPONSE_BYTES", 25 * 1024 * 1024)
    kwargs = {"headers": headers}
    if data is not None:
        kwargs["data"] = data
    async with client.stream(method, url, **kwargs) as resp:
        buf = bytearray()
        async for chunk in resp.aiter_bytes():   # aiter_bytes yields DECODED bytes
            buf += chunk
            if len(buf) > max_bytes:
                del buf[max_bytes:]
                break
        resp._content = bytes(buf)
        return resp


class Request:
    """A single HTTP request.

    The actual network I/O is delegated to a shared :class:`httpx.AsyncClient`
    passed to :meth:`get_response`.
    """

    SAFE_CHARS = "%/:=&?~#+!$,;'@()*[]|"

    def __init__(self, url=None, headers=None):
        self.url = url
        self.headers = dict(headers or {})
        self.headers.setdefault("User-Agent", config.MOZILLA_USER_AGENT)
        self.headers.setdefault(
            "Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
        )
        self.headers.setdefault("Accept-Language", "es-419,es;q=0.8,en;q=0.6")

    def _normalize_url(self):
        """Quote unsafe characters in the request url."""
        self.url = urllib.parse.quote(self.url, safe=self.SAFE_CHARS)

    async def get_response(self, client, data=None, delay_factor=1):
        """Perform the request and return the ``httpx`` response.

        A POST is issued when *data* is provided, otherwise a GET.
        """
        self._normalize_url()

        # Size-capped streaming for the httpx path (the default), for BOTH GET and
        # POST, so a huge/mislabeled body can't OOM the box. Non-httpx clients
        # (curl_cffi impersonate/stealth) cap the body themselves.
        if isinstance(client, httpx.AsyncClient):
            method = "POST" if data is not None else "GET"
            return await _capped_stream(client, method, self.url, self.headers, data=data)
        if data is not None:
            return await client.post(self.url, data=data, headers=self.headers)
        return await client.get(self.url, headers=self.headers)


class DelayedRequest(Request):
    """A request that waits a (randomized) delay before hitting the network."""

    def __init__(self, delay=0, deviation=0, **kwargs):
        randomize = random.uniform(-deviation, deviation)
        self.delay = max(0.0, delay + randomize)
        super().__init__(**kwargs)

    async def get_response(self, client, data=None, delay_factor=1):
        await asyncio.sleep(self.delay * delay_factor)
        return await super().get_response(client, data, delay_factor)
