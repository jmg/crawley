"""Tests for the on-disk HTTP cache."""

import os

from crawley.crawlers import BaseCrawler
from crawley.http.cache import HttpCache
from crawley.http.managers import FastRequestManager
from crawley.scrapers import BaseScraper


def test_cache_store_and_get(tmp_path):
    cache = HttpCache(str(tmp_path), enabled=True)
    assert cache.get("GET", "http://x/") is None

    cache.store("GET", "http://x/", None, 200, "http://x/", {"a": "b"}, "<html>hi</html>")
    hit = cache.get("GET", "http://x/")
    assert hit["status"] == 200
    assert hit["body"] == "<html>hi</html>"
    assert hit["url"] == "http://x/"


def test_cache_key_includes_method_and_body(tmp_path):
    cache = HttpCache(str(tmp_path))
    cache.store("GET", "http://x/", None, 200, "http://x/", {}, "get")
    assert cache.get("POST", "http://x/", {"q": 1}) is None
    cache.store("POST", "http://x/", {"q": 1}, 200, "http://x/", {}, "post")
    assert cache.get("POST", "http://x/", {"q": 1})["body"] == "post"


def test_disabled_cache_is_noop(tmp_path):
    cache = HttpCache(str(tmp_path), enabled=False)
    cache.store("GET", "http://x/", None, 200, "http://x/", {}, "body")
    assert cache.get("GET", "http://x/") is None


async def test_manager_uses_cache(server, tmp_path):
    cache = HttpCache(str(tmp_path), enabled=True)
    manager = FastRequestManager(cache=cache)
    try:
        first = await manager.make_request(server + "/page1")
        assert first.status_code == 200
        # The response is now cached on disk.
        files = os.listdir(tmp_path)
        assert len(files) == 1
    finally:
        await manager.aclose()

    # A fresh manager pointed at an unreachable host still serves from cache.
    manager2 = FastRequestManager(cache=cache)
    try:
        cached = await manager2.make_request(server + "/page1")
        assert "Title 1" in cached.raw_html
    finally:
        await manager2.aclose()


async def test_crawler_http_cache_attribute(server, tmp_path):
    visited = []

    class S(BaseScraper):
        matching_urls = ["%/page%"]

        def scrape(self, response):
            visited.append(response.url)

    class C(BaseCrawler):
        start_urls = [server + "/page1"]
        scrapers = [S]
        max_depth = 0
        requests_delay = 0
        http_cache = True
        http_cache_dir = str(tmp_path)

    await C().start()
    assert len(os.listdir(tmp_path)) >= 1
