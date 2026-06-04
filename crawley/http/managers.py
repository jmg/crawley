"""Request managers orchestrating the HTTP layer."""

import urllib.parse

import httpx

from crawley import config
from crawley.http.cookies import CookieHandler
from crawley.http.request import DelayedRequest, Request
from crawley.http.response import Response
from crawley.utils import has_valid_attr


class HostCounterDict(dict):
    """A counter dictionary for requested hosts."""

    def increase(self, key):
        self[key] = self.get(key, 0) + 1

    def count(self, key):
        return self.setdefault(key, 0)


class RequestManager:
    """Manage HTTP requests through a shared :class:`httpx.AsyncClient`."""

    MAX_TRIES = config.REQUEST_MAX_RETRIES

    def __init__(self, settings=None, headers=None, delay=None, deviation=None):
        self.host_counter = HostCounterDict()
        self.cookie_handler = CookieHandler()
        self.cookie_handler.load_cookies()
        self.headers = headers or {}
        self.delay = delay if delay is not None else config.REQUEST_DELAY
        self.deviation = (
            deviation if deviation is not None else config.REQUEST_DEVIATION
        )
        self.settings = settings
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

    def _get_request(self, url):
        host = urllib.parse.urlparse(url).netloc
        self.host_counter.increase(host)
        return DelayedRequest(
            url=url,
            headers=self.headers,
            delay=self.delay,
            deviation=self.deviation,
        )

    async def make_request(self, url, data=None, extractor=None):
        """Issue a request and wrap the result in a :class:`Response`."""
        request = self._get_request(url)
        response = await self.get_response(request, data)

        raw_html = response.text

        extracted_html = None
        if extractor is not None:
            extracted_html = extractor.get_object(raw_html)

        return Response(
            raw_html=raw_html,
            extracted_html=extracted_html,
            url=str(response.url),
            response=response,
        )

    async def get_response(self, request, data):
        """Try ``MAX_TRIES`` times to perform the request."""
        last_exc = None

        for tries in range(self.MAX_TRIES + 1):
            try:
                return await request.get_response(
                    self.client, data, delay_factor=tries
                )
            except Exception as ex:  # noqa: BLE001 - retried below
                last_exc = ex

        raise last_exc


class FastRequestManager(RequestManager):
    """A request manager without per-request delays."""

    def _get_request(self, url):
        host = urllib.parse.urlparse(url).netloc
        self.host_counter.increase(host)
        return Request(url=url, headers=self.headers)
