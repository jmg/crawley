"""Tests for robots.txt support."""

import httpx

from crawley.crawlers import BaseCrawler
from crawley.http.robots import RobotsPolicy
from crawley.scrapers import BaseScraper


class FakeResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.calls = 0

    async def get(self, url):
        self.calls += 1
        return self.response


async def test_disabled_policy_allows_everything():
    policy = RobotsPolicy(enabled=False)
    assert await policy.allowed("http://x/private", client=None) is True


async def test_allowed_and_disallowed(server):
    policy = RobotsPolicy(user_agent="*")
    async with httpx.AsyncClient() as client:
        assert await policy.allowed(server + "/page1", client) is True
        assert await policy.allowed(server + "/private/secret", client) is False


async def test_missing_robots_allows_all():
    policy = RobotsPolicy()
    client = FakeClient(FakeResponse(404))
    assert await policy.allowed("http://x.test/anything", client) is True


async def test_forbidden_robots_disallows_all():
    policy = RobotsPolicy()
    client = FakeClient(FakeResponse(403))
    assert await policy.allowed("http://x.test/anything", client) is False


async def test_robots_is_cached():
    policy = RobotsPolicy()
    client = FakeClient(FakeResponse(200, "User-agent: *\nDisallow: /no\n"))
    assert await policy.allowed("http://x.test/yes", client) is True
    assert await policy.allowed("http://x.test/no", client) is False
    # Only one network call for the host.
    assert client.calls == 1


async def test_crawl_delay_parsed():
    policy = RobotsPolicy(user_agent="*")
    client = FakeClient(
        FakeResponse(200, "User-agent: *\nCrawl-delay: 2\nDisallow:\n")
    )
    await policy.allowed("http://x.test/a", client)
    assert policy.crawl_delay("http://x.test/a") == 2.0


async def test_crawler_respects_robots(server):
    blocked = []
    scraped = []

    class S(BaseScraper):
        matching_urls = ["%"]

        def scrape(self, response):
            scraped.append(response.url)

    class C(BaseCrawler):
        start_urls = [server + "/page1", server + "/private/secret"]
        scrapers = [S]
        max_depth = 0
        respect_robots = True
        requests_delay = 0
        requests_deviation = 0

        def on_robots_blocked(self, url):
            blocked.append(url)

    await C().start()

    assert any("/page1" in u for u in scraped)
    assert any("/private/secret" in u for u in blocked)
    assert not any("/private" in u for u in scraped)
