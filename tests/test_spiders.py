"""Tests for LinkExtractor, CrawlSpider and SitemapSpider."""

from crawley.http.response import Response
from crawley.spiders import CrawlSpider, LinkExtractor, Rule, SitemapSpider

HTML = """
<html><body>
  <div id="nav"><a href="/page/2/">2</a><a href="/page/3/">3</a></div>
  <div id="content"><a href="/item/a">a</a><a href="/about">about</a></div>
</body></html>
"""


def _response(url="http://site.test/"):
    return Response(raw_html=HTML, url=url)


def test_link_extractor_allow_deny():
    le = LinkExtractor(allow=[r"/page/"], deny=[r"/page/3"])
    links = le.extract_links(_response())
    assert "http://site.test/page/2/" in links
    assert "http://site.test/page/3/" not in links
    assert "http://site.test/item/a" not in links


def test_link_extractor_restrict_css():
    le = LinkExtractor(restrict_css=["#content"])
    links = le.extract_links(_response())
    assert "http://site.test/item/a" in links
    assert "http://site.test/page/2/" not in links


def test_link_extractor_unique():
    html = '<html><body><a href="/x">1</a><a href="/x">2</a></body></html>'
    le = LinkExtractor()
    links = le.extract_links(Response(raw_html=html, url="http://s/"))
    assert links == ["http://s/x"]


async def test_crawlspider_rules(quotes_server):
    items = []

    class QuotesCrawl(CrawlSpider):
        start_urls = [quotes_server]
        requests_delay = 0
        requests_deviation = 0
        rules = [
            Rule(
                LinkExtractor(allow=[r"/page/\d+/"]),
                callback="parse_page",
                follow=True,
            ),
        ]

        def parse_page(self, response):
            for quote in response.css("div.quote"):
                yield {"text": quote.css_first("span.text").text}

        def on_item(self, item):
            items.append(item["text"])

    await QuotesCrawl().start()

    # Pages 2 and 3 reached by following the pager (page 1 is the seed and is
    # only parsed for links, not by the rule callback).
    assert any("Quote 2-1" == t for t in items)
    assert any("Quote 3-1" == t for t in items)


async def test_sitemap_spider(quotes_server):
    pages = []

    class QuotesSitemap(SitemapSpider):
        sitemap_urls = [quotes_server + "sitemap.xml"]
        requests_delay = 0
        requests_deviation = 0

        def parse(self, response):
            pages.append(response.url)

    await QuotesSitemap().start()

    assert len(pages) == 3
    assert any(p.endswith("/page/2/") for p in pages)
