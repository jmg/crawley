"""Request managers orchestrating the HTTP layer."""

import urllib.parse

import httpx

from crawley import config
from crawley.http import urlguard
from crawley.http.cookies import CookieHandler
from crawley.http.request import DelayedRequest, Request
from crawley.http.response import Response
from crawley.http.retry import RetryPolicy
from crawley.http.throttle import HostRateLimiter
from crawley.utils import has_valid_attr


async def _ssrf_request_hook(request):
    """Abort any request (incl. a redirect hop) to a non-public/internal host.

    Runs the active :func:`crawley.http.urlguard.current_guard` on every request
    URL. Installed only when ``SSRF_PROTECT`` is enabled (see
    :meth:`RequestManager._build_client_kwargs`), so it costs nothing by default.
    """
    if not urlguard.current_guard()(str(request.url)):
        raise httpx.RequestError(
            "Blocked non-public/SSRF URL: %s" % request.url, request=request
        )


class HostCounterDict(dict):
    """A counter dictionary for requested hosts."""

    def increase(self, key):
        self[key] = self.get(key, 0) + 1

    def count(self, key):
        return self.setdefault(key, 0)


class RequestManager:
    """Manage HTTP requests through a shared :class:`httpx.AsyncClient`."""

    def __init__(
        self,
        settings=None,
        headers=None,
        delay=None,
        deviation=None,
        retry_policy=None,
        rate_limiter=None,
        cache=None,
    ):
        self.host_counter = HostCounterDict()
        self.cookie_handler = CookieHandler()
        self.cookie_handler.load_cookies()
        self.headers = headers or {}
        self.delay = delay if delay is not None else config.REQUEST_DELAY
        self.deviation = (
            deviation if deviation is not None else config.REQUEST_DEVIATION
        )
        self.settings = settings
        self.retry_policy = retry_policy if retry_policy is not None else RetryPolicy()
        self.rate_limiter = (
            rate_limiter if rate_limiter is not None else HostRateLimiter()
        )
        self.cache = cache
        self._client = None
        # Opt-in SSRF protection (block private/loopback/metadata targets incl.
        # redirect hops). Off by default so local-dev crawls of localhost work;
        # a host app enables it via a ``SSRF_PROTECT`` setting or config default.
        self.ssrf_protect = bool(
            getattr(self.settings, "SSRF_PROTECT", config.SSRF_PROTECT)
        )
        # Optional pool of proxy URLs, rotated per request.
        self.proxy_pool = list(getattr(self.settings, "PROXY_POOL", None) or [])
        self._pool_clients = {}
        self._proxy_rr = 0

    # -- client lifecycle ------------------------------------------------

    def _proxy_url(self, proxy=None):
        """The proxy URL for a request: an explicit one, else the settings' single
        managed proxy (PROXY_HOST/PORT/USER/PASS), else None."""
        if proxy:
            return proxy
        if has_valid_attr(self.settings, "PROXY_HOST") and has_valid_attr(
            self.settings, "PROXY_PORT"
        ):
            user = getattr(self.settings, "PROXY_USER", "")
            password = getattr(self.settings, "PROXY_PASS", "")
            host = getattr(self.settings, "PROXY_HOST", "")
            port = getattr(self.settings, "PROXY_PORT", 80)
            auth = "%s:%s@" % (user, password) if user else ""
            return "http://%s%s:%s" % (auth, host, port)
        return None

    def _build_client_kwargs(self, proxy=None):
        kwargs = {
            "cookies": self.cookie_handler.jar,
            "follow_redirects": True,
            "timeout": config.REQUEST_TIMEOUT,
        }
        if self.ssrf_protect:
            # Re-validate every request URL incl. redirect hops. The hook inspects
            # request.url (no TCP connect), so it's kept even when proxied.
            kwargs["event_hooks"] = {"request": [_ssrf_request_hook]}
        p = self._proxy_url(proxy)
        if p:
            kwargs["proxy"] = p
        return kwargs

    def _make_client(self, proxy=None):
        """Build the HTTP client for a request.

        With ``settings.IMPERSONATE`` set (crawler stealth) and the optional
        ``curl_cffi`` dependency installed, use an
        :class:`~crawley.http.impersonate.ImpersonateClient` for a real browser
        TLS/JA3 fingerprint; it preserves the same per-hop SSRF guard. Falls back
        to ``httpx`` if ``curl_cffi`` isn't installed.
        """
        imp = getattr(self.settings, "IMPERSONATE", None)
        if imp:
            try:
                from crawley.http.impersonate import ImpersonateClient

                return ImpersonateClient(
                    impersonate=imp,
                    proxy=self._proxy_url(proxy),
                    timeout=config.REQUEST_TIMEOUT,
                    ssrf_protect=self.ssrf_protect,
                )
            except Exception:
                pass  # curl_cffi missing / import error → plain httpx
        return httpx.AsyncClient(**self._build_client_kwargs(proxy=proxy))

    @property
    def client(self):
        if self._client is None:
            self._client = self._make_client()
        return self._client

    def _client_for(self, proxy):
        if proxy not in self._pool_clients:
            self._pool_clients[proxy] = self._make_client(proxy=proxy)
        return self._pool_clients[proxy]

    def select_client(self):
        """Return the client for the next request, rotating the proxy pool."""
        if not self.proxy_pool:
            return self.client
        proxy = self.proxy_pool[self._proxy_rr % len(self.proxy_pool)]
        self._proxy_rr += 1
        return self._client_for(proxy)

    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()
            self._client = None
        for client in self._pool_clients.values():
            await client.aclose()
        self._pool_clients = {}
        self.cookie_handler.save_cookies()

    # -- requests --------------------------------------------------------

    def _get_request(self, url, headers=None):
        host = urllib.parse.urlparse(url).netloc
        self.host_counter.increase(host)
        merged = {**self.headers, **(headers or {})}
        return DelayedRequest(
            url=url,
            headers=merged,
            delay=self.delay,
            deviation=self.deviation,
        )

    async def make_request(self, url, data=None, extractor=None, headers=None):
        """Issue a request and wrap the result in a :class:`Response`."""
        method = "POST" if data is not None else "GET"

        if self.cache is not None:
            cached = self.cache.get(method, url, data)
            if cached is not None:
                return self._response_from_cache(cached, extractor)

        request = self._get_request(url, headers)
        host = urllib.parse.urlparse(url).netloc

        semaphore = self.rate_limiter.semaphore(host)
        if semaphore is not None:
            await semaphore.acquire()
        try:
            await self.rate_limiter.throttle(host)
            response = await self.get_response(request, data)
        finally:
            if semaphore is not None:
                semaphore.release()

        raw_html = response.text
        final_url = str(response.url)

        if getattr(self.settings, "AUTOTHROTTLE", False):
            self._autothrottle(host, getattr(response, "status_code", 200))

        # Only cache success / redirect responses. The cache has no TTL, so
        # storing a transient 429/500/503 (or any error) would replay that
        # failure on every later run for the same url — turning a momentary blip
        # into permanent, silent data loss.
        if self.cache is not None and 200 <= (response.status_code or 0) < 400:
            self.cache.store(
                method, url, data, response.status_code, final_url,
                dict(response.headers), raw_html,
            )

        extracted_html = None
        if extractor is not None:
            extracted_html = extractor.get_object(raw_html)

        result = Response(
            raw_html=raw_html,
            extracted_html=extracted_html,
            url=final_url,
            response=response,
        )
        elapsed = getattr(response, "elapsed", None)
        if elapsed is not None:
            result.latency = elapsed.total_seconds()
        return result

    @staticmethod
    def _response_from_cache(cached, extractor):
        from crawley.http.cache import _CachedResponse

        raw_html = cached["body"]
        extracted = extractor.get_object(raw_html) if extractor is not None else None
        return Response(
            raw_html=raw_html,
            extracted_html=extracted,
            url=cached["url"],
            response=_CachedResponse(cached["status"], cached["headers"]),
        )

    # Adaptive per-host politeness (a Scrapy AutoThrottle analog): back off when
    # the target pushes back, relax toward the base delay when it's healthy —
    # bounded so it can never stall a crawl indefinitely.
    AUTOTHROTTLE_MAX = 15.0

    def _autothrottle(self, host, status):
        base = self.rate_limiter.delay
        cur = self.rate_limiter._delay_for(host)
        # Only the unambiguous overload codes — 403 is usually a hard block on a
        # SUBSET of a host's URLs (auth/WAF/hotlink), so throttling the whole host
        # on it both false-positives and doesn't help (a ban needs a new IP, not a
        # slower one). Never cap below the user's own delay (ceiling honors base).
        if status in (429, 503):
            new = min(max(cur, 0.5) * 2.0, max(self.AUTOTHROTTLE_MAX, base))  # slow down hard
        elif cur > base:
            new = max(base, cur * 0.9)  # healthy → ease back toward the base delay
        else:
            return
        self.rate_limiter.set_delay(host, new)

    async def get_response(self, request, data):
        """Perform the request, retrying with backoff per the retry policy."""
        attempt = 0

        while True:
            try:
                response = await request.get_response(self.select_client(), data)
            except Exception as ex:  # noqa: BLE001 - decided by the retry policy
                if self.retry_policy.should_retry(attempt, exception=ex):
                    await self.retry_policy.sleep(
                        self.retry_policy.backoff_time(attempt)
                    )
                    attempt += 1
                    continue
                raise

            if self.retry_policy.should_retry(attempt, response=response):
                await self.retry_policy.sleep(
                    self.retry_policy.backoff_time(attempt, response)
                )
                attempt += 1
                continue

            return response


class FastRequestManager(RequestManager):
    """A request manager without per-request delays."""

    def _get_request(self, url, headers=None):
        host = urllib.parse.urlparse(url).netloc
        self.host_counter.increase(host)
        merged = {**self.headers, **(headers or {})}
        return Request(url=url, headers=merged)
