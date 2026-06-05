"""Request managers orchestrating the HTTP layer."""

import urllib.parse

import httpx

from crawley import config
from crawley.http.cookies import CookieHandler
from crawley.http.request import DelayedRequest, Request
from crawley.http.response import Response
from crawley.http.retry import RetryPolicy
from crawley.http.throttle import HostRateLimiter
from crawley.utils import has_valid_attr


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

    # -- client lifecycle ------------------------------------------------

    def _build_client_kwargs(self):
        kwargs = {
            "cookies": self.cookie_handler.jar,
            "follow_redirects": True,
            "timeout": config.REQUEST_TIMEOUT,
        }

        if has_valid_attr(self.settings, "PROXY_HOST") and has_valid_attr(
            self.settings, "PROXY_PORT"
        ):
            user = getattr(self.settings, "PROXY_USER", "")
            password = getattr(self.settings, "PROXY_PASS", "")
            host = getattr(self.settings, "PROXY_HOST", "")
            port = getattr(self.settings, "PROXY_PORT", 80)
            auth = "%s:%s@" % (user, password) if user else ""
            kwargs["proxy"] = "http://%s%s:%s" % (auth, host, port)

        return kwargs

    @property
    def client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(**self._build_client_kwargs())
        return self._client

    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()
            self._client = None
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

        if self.cache is not None:
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

    async def get_response(self, request, data):
        """Perform the request, retrying with backoff per the retry policy."""
        attempt = 0

        while True:
            try:
                response = await request.get_response(self.client, data)
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
