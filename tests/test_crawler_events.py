"""Tests for crawler events, login and error handling."""

import pytest

from crawley.crawlers import BaseCrawler
from crawley.exceptions import AuthenticationError


async def test_on_start_and_on_finish(server):
    events = []

    class C(BaseCrawler):
        start_urls = [server + "/"]
        max_depth = 0
        requests_delay = 0

        def on_start(self):
            events.append("start")

        def on_finish(self):
            events.append("finish")

    await C().start()
    assert events == ["start", "finish"]


async def test_request_error_handler():
    errors = []

    class C(BaseCrawler):
        start_urls = ["http://127.0.0.1:1/unreachable"]
        max_depth = 0
        requests_delay = 0

        def on_request_error(self, url, ex):
            errors.append(url)

    crawler = C()
    crawler.request_manager.retry_policy.max_retries = 0
    await crawler.start()
    assert errors == ["http://127.0.0.1:1/unreachable"]


async def test_login_success(server):
    class C(BaseCrawler):
        start_urls = []
        login = (server + "/", {"user": "x"})
        requests_delay = 0

    # Should not raise.
    await C().start()


async def test_login_failure(server):
    class C(BaseCrawler):
        start_urls = []
        login = (server + "/", {"user": "x"})
        requests_delay = 0

        async def _get_response(self, url, data=None):
            return None

    with pytest.raises(AuthenticationError):
        await C().start()


async def test_search_all_urls_disabled(server):
    fetched = []

    class C(BaseCrawler):
        start_urls = [server + "/"]
        scrapers = []
        max_depth = 5
        search_all_urls = False
        requests_delay = 0

        def _manage_scrapers(self, response):
            fetched.append(response.url)
            return super()._manage_scrapers(response)

    await C().start()
    # With link discovery disabled and no scrapers, only the start url is hit.
    assert len(fetched) == 1
