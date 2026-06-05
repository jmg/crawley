"""Async HTTP request objects built on top of ``httpx``."""

import asyncio
import random
import urllib.parse

from crawley import config


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
