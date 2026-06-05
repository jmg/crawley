"""Tests for the stats collector and its integration."""

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.spider import Spider
from crawley.stats import StatsCollector


def test_stats_collector_basics():
    stats = StatsCollector()
    stats.open()
    stats.inc("requests")
    stats.inc("requests", 2)
    stats.set("foo", "bar")
    stats.close()

    assert stats.get("requests") == 3
    assert stats.get("foo") == "bar"
    assert "elapsed_seconds" in stats.get_stats()
    assert stats.get("missing", 0) == 0


async def test_crawler_collects_stats(server):
    class S(BaseScraper):
        matching_urls = ["%/page%"]

        def scrape(self, response):
            pass

    class C(BaseCrawler):
        start_urls = [server + "/"]
        scrapers = [S]
        max_depth = 1
        requests_delay = 0
        requests_deviation = 0

    crawler = C()
    await crawler.start()

    stats = crawler.stats.get_stats()
    assert stats["requests"] >= 3
    assert stats["responses"] >= 3
    assert stats.get("status/200", 0) >= 3
    assert "elapsed_seconds" in stats


async def test_spider_collects_item_stats(quotes_server):
    from crawley.pipelines import DropItem, ItemPipeline

    class DropFirst(ItemPipeline):
        def process_item(self, item, spider):
            if item["text"].endswith("1-1"):
                raise DropItem()
            return item

    class QSpider(Spider):
        start_urls = [quotes_server]
        pipelines = [DropFirst]
        requests_delay = 0

        def parse(self, response):
            for quote in response.css("div.quote"):
                yield {"text": quote.css_first("span.text").text}
            nxt = response.css_first("li.next a")
            if nxt:
                yield response.follow(nxt.attr("href"))

    spider = QSpider()
    await spider.start()

    stats = spider.stats.get_stats()
    assert stats["items"] == 5  # 6 quotes minus the dropped one
    assert stats["items_dropped"] == 1
    assert stats["responses"] == 3


async def test_request_error_stat():
    class C(BaseCrawler):
        start_urls = ["http://127.0.0.1:1/down"]
        max_depth = 0
        requests_delay = 0

    crawler = C()
    crawler.request_manager.retry_policy.max_retries = 0
    await crawler.start()
    assert crawler.stats.get("request_errors") == 1
