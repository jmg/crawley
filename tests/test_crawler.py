"""End-to-end crawler tests against the local server."""

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper


def _make_crawler(server, **attrs):
    collected = []

    class _Scraper(BaseScraper):
        matching_urls = ["%/page%"]

        def scrape(self, response):
            collected.append(response.html.xpath("//h1")[0].text)

    attrs.setdefault("scrapers", [_Scraper])
    attrs.setdefault("requests_delay", 0)
    attrs.setdefault("requests_deviation", 0)
    attrs.setdefault("start_urls", [server + "/"])
    crawler = type("_Crawler", (BaseCrawler,), attrs)()
    return crawler, collected


async def test_basic_crawl(server):
    crawler, collected = _make_crawler(server, max_depth=1)
    await crawler.start()
    # page1, page2 and page3 each carry an <h1> the scraper collects.
    assert any("Title 1" in t for t in collected)
    assert any("Title 2" in t for t in collected)


async def test_max_depth_zero(server):
    crawler, collected = _make_crawler(server, max_depth=0)
    await crawler.start()
    # Depth 0: only the start url is fetched, which has no matching scraper.
    assert collected == []


async def test_black_list(server):
    crawler, collected = _make_crawler(
        server, max_depth=1, black_list=["%/page2%"]
    )
    await crawler.start()
    assert any("Title 1" in t for t in collected)
    assert not any("Title 2" in t for t in collected)


async def test_allowed_urls(server):
    crawler, collected = _make_crawler(
        server, max_depth=1, allowed_urls=["%/page1", "%/"]
    )
    await crawler.start()
    assert any("Title 1" in t for t in collected)
    assert not any("Title 2" in t for t in collected)


async def test_post_urls(server):
    crawler, _ = _make_crawler(
        server,
        max_depth=0,
        scrapers=[],
        start_urls=[server + "/echo"],
        post_urls=[("%/echo%", {"hello": "world"})],
    )
    response = await crawler._get_response(server + "/echo")
    assert "hello=world" in response.raw_html
    await crawler.request_manager.aclose()
