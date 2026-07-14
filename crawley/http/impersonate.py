"""Real browser TLS / JA3 fingerprint for crawl requests, via ``curl_cffi``.

Header-only "stealth" on vanilla ``httpx`` is trivially flagged: anti-bot
services fingerprint the **TLS handshake (JA3)** and the **HTTP/2 frame order**,
neither of which a User-Agent header changes. When a crawler opts in
(``IMPERSONATE = "chrome"`` on its settings) and the optional ``curl_cffi``
dependency is installed, the :class:`~crawley.http.managers.RequestManager` swaps
its ``httpx`` client for this adapter, which mimics a real Chrome's TLS/HTTP2
fingerprint.

Install the extra with ``pip install crawley[impersonate]``.

The adapter exposes exactly the surface the manager uses
(``get`` / ``post`` / ``aclose`` and a response with
``text`` / ``status_code`` / ``url`` / ``headers`` / ``elapsed``) so it is a
drop-in for ``httpx.AsyncClient``. SSRF protection is preserved: ``curl_cffi``
follows redirects internally, so we disable that and follow **manually**, running
the active :func:`crawley.http.urlguard.current_guard` on every hop.
"""

import datetime
import urllib.parse

from crawley import config
from crawley.http import urlguard

__all__ = ["ImpersonateClient", "is_available", "DEFAULT_IMPERSONATE"]

#: The default browser profile passed to ``curl_cffi``.
DEFAULT_IMPERSONATE = "chrome"

_REDIRECT_CODES = (301, 302, 303, 307, 308)
_MAX_HOPS = 8


def is_available():
    """Return ``True`` if the optional ``curl_cffi`` dependency is importable."""
    try:
        import curl_cffi  # noqa: F401

        return True
    except Exception:
        return False


class _Resp:
    """Adapt a ``curl_cffi`` response to the ``httpx``-response surface the manager reads.

    Built from a streamed response plus the already-read (size-capped) body text,
    so it never re-reads the whole body into memory.
    """

    def __init__(self, r, text):
        self.text = text
        self.status_code = r.status_code
        self.url = str(r.url)
        self.headers = r.headers
        el = getattr(r, "elapsed", 0) or 0
        # The manager calls ``response.elapsed.total_seconds()``; ``curl_cffi``
        # gives a float, ``httpx`` a timedelta — normalize to a timedelta.
        self.elapsed = (
            el if hasattr(el, "total_seconds") else datetime.timedelta(seconds=float(el))
        )


class ImpersonateClient:
    """An ``httpx.AsyncClient``-compatible client backed by ``curl_cffi``.

    Provides a real browser TLS fingerprint plus per-hop SSRF checks. Only the
    ``get`` / ``post`` / ``aclose`` methods used by the request manager are
    implemented.

    Args:
        impersonate: A ``curl_cffi`` browser profile (e.g. ``"chrome"``).
        proxy: Optional proxy URL applied to both http and https.
        timeout: Per-request timeout in seconds.
        ssrf_protect: When ``True``, run the active
            :func:`crawley.http.urlguard.current_guard` on every hop and refuse
            non-public targets — matching the ``httpx`` path's ``SSRF_PROTECT``.
    """

    def __init__(
        self, impersonate=DEFAULT_IMPERSONATE, proxy=None, timeout=30, ssrf_protect=False
    ):
        from curl_cffi.requests import AsyncSession

        self._session = AsyncSession()
        self._impersonate = impersonate or DEFAULT_IMPERSONATE
        self._proxies = {"http": proxy, "https": proxy} if proxy else None
        self._timeout = timeout
        self._ssrf_protect = ssrf_protect

    async def get(self, url, headers=None):
        return await self._request("GET", url, headers=headers)

    async def post(self, url, data=None, headers=None):
        return await self._request("POST", url, data=data, headers=headers)

    async def _request(self, method, url, headers=None, data=None, _hops=0):
        if self._ssrf_protect and not urlguard.current_guard()(url):
            raise RuntimeError("Blocked non-public/SSRF URL: %s" % url)
        resp = await self._session.request(
            method,
            url,
            headers=headers,
            data=data,
            impersonate=self._impersonate,
            proxies=self._proxies,
            allow_redirects=False,
            timeout=self._timeout,
            stream=True,  # read the body ourselves, bounded by MAX_RESPONSE_BYTES
        )
        try:
            if resp.status_code in _REDIRECT_CODES and _hops < _MAX_HOPS:
                loc = resp.headers.get("location") or resp.headers.get("Location")
                if loc:
                    nxt = urllib.parse.urljoin(url, loc)
                    # 303, and legacy 301/302 after a POST, redirect to a bodyless GET.
                    if resp.status_code == 303 or (
                        resp.status_code in (301, 302) and method == "POST"
                    ):
                        return await self._request("GET", nxt, headers=headers, _hops=_hops + 1)
                    return await self._request(
                        method, nxt, headers=headers, data=data, _hops=_hops + 1
                    )
            # Final response: read the body with a hard size cap (mirrors the
            # httpx path's MAX_RESPONSE_BYTES) so a huge/mislabeled body — a media
            # file caught by a link-follow — can't OOM the process.
            return _Resp(resp, await self._read_capped(resp))
        finally:
            # Release the connection whether we followed a redirect (body unread)
            # or finished reading the final response.
            close = getattr(resp, "aclose", None)
            if close is not None:
                try:
                    await close()
                except Exception:
                    pass

    async def _read_capped(self, resp):
        max_bytes = getattr(config, "MAX_RESPONSE_BYTES", 25 * 1024 * 1024)
        buf = bytearray()
        async for chunk in resp.aiter_content():
            buf += bytes(chunk)
            if len(buf) > max_bytes:
                del buf[max_bytes:]
                break
        enc = getattr(resp, "encoding", None) or "utf-8"
        try:
            return bytes(buf).decode(enc, errors="replace")
        except LookupError:
            return bytes(buf).decode("utf-8", errors="replace")

    async def aclose(self):
        try:
            await self._session.close()
        except Exception:
            pass
