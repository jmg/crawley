"""Tests for the Playwright (JS rendering) integration.

Playwright itself (and a browser) isn't required: the rendering step is
monkeypatched, so these tests exercise the wiring without launching a browser.
"""

from crawley.extractors import XPathExtractor
from crawley.http.playwright import PlaywrightRequestManager
from crawley.spider import Spider

RENDERED = "<html><body><h1>Rendered by JS</h1><a href='/x'>x</a></body></html>"


def test_render_js_selects_playwright_manager():
    class S(Spider):
        render_js = True
        start_urls = []

    spider = S()
    assert isinstance(spider.request_manager, PlaywrightRequestManager)


def test_plain_crawler_does_not_use_playwright():
    from crawley.http.managers import RequestManager

    class S(Spider):
        start_urls = []

    spider = S()
    assert type(spider.request_manager) is RequestManager


async def test_make_request_builds_response_from_render():
    manager = PlaywrightRequestManager()

    async def fake_render(url, headers=None):
        return RENDERED, url, 200

    manager._render = fake_render

    response = await manager.make_request(
        "http://spa.test/", extractor=XPathExtractor()
    )
    assert response.status_code == 200
    assert response.css_first("h1").text == "Rendered by JS"
    await manager.aclose()  # no browser was launched -> safe


async def test_render_with_retry_recovers(monkeypatch):
    import httpx

    from crawley.http.retry import RetryPolicy

    manager = PlaywrightRequestManager(
        retry_policy=RetryPolicy(max_retries=2, backoff_factor=0)
    )
    calls = {"n": 0}

    async def flaky_render(url, headers=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("boom")
        return RENDERED, url, 200

    manager._render = flaky_render
    response = await manager.make_request("http://spa.test/")
    assert response.status_code == 200
    assert calls["n"] == 2
    await manager.aclose()


async def test_spider_render_end_to_end():
    class S(Spider):
        render_js = True
        start_urls = ["http://spa.test/"]
        requests_delay = 0

        def parse(self, response):
            self.title = response.css_first("h1").text

    spider = S()

    async def fake_render(url, headers=None):
        return RENDERED, url, 200

    spider.request_manager._render = fake_render
    await spider.start()
    assert spider.title == "Rendered by JS"
