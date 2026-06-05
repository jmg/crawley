"""Tests for the callback-driven Spider, Request and item pipelines."""

from crawley.pipelines import DropItem, ItemPipeline
from crawley.spider import Request, Spider


def test_request_fingerprint_and_replace():
    a = Request("http://x/", method="get")
    assert a.method == "GET"
    b = Request("http://x/")
    assert a.fingerprint() == b.fingerprint()
    assert Request("http://x/", data="q=1").fingerprint() != a.fingerprint()

    c = a.replace(url="http://y/")
    assert c.url == "http://y/" and a.url == "http://x/"


async def test_spider_follows_pagination_and_emits_items(quotes_server):
    items = []

    class QSpider(Spider):
        start_urls = [quotes_server]
        requests_delay = 0
        requests_deviation = 0

        def parse(self, response):
            for quote in response.css("div.quote"):
                yield {
                    "text": quote.css_first("span.text").text,
                    "depth": response.meta.get("depth"),
                }
            nxt = response.css_first("li.next a")
            if nxt:
                yield response.follow(nxt.attr("href"))

        def on_item(self, item):
            items.append(item)

    await QSpider().start()

    assert len(items) == 6
    assert {it["depth"] for it in items} == {0, 1, 2}


async def test_meta_and_cb_kwargs(quotes_server):
    class MSpider(Spider):
        start_urls = [quotes_server]
        requests_delay = 0

        def parse(self, response):
            yield response.follow(
                "/page/2/", callback=self.parse_2,
                meta={"tag": "x"}, cb_kwargs={"n": 42},
            )

        def parse_2(self, response, n=None):
            self.captured = (response.meta.get("tag"), n)

    spider = MSpider()
    await spider.start()
    assert spider.captured == ("x", 42)


async def test_pipeline_transforms_and_drops(quotes_server):
    kept = []

    class OnlyFirst(ItemPipeline):
        def open_spider(self, spider):
            spider.opened = True

        def process_item(self, item, spider):
            if item["text"].endswith("1-2"):
                raise DropItem()
            item["text"] = item["text"].upper()
            return item

    class QSpider(Spider):
        start_urls = [quotes_server]
        pipelines = [OnlyFirst]
        requests_delay = 0

        def parse(self, response):
            for quote in response.css("div.quote"):
                yield {"text": quote.css_first("span.text").text}

        def on_item(self, item):
            kept.append(item["text"])

    spider = QSpider()
    await spider.start()

    assert spider.opened is True
    assert "QUOTE 1-1" in kept
    assert all(not t.endswith("1-2") for t in kept)  # dropped items


async def test_dont_filter_allows_duplicates(quotes_server):
    hits = []

    class DSpider(Spider):
        start_urls = [quotes_server]
        requests_delay = 0

        def start_requests(self):
            yield Request(quotes_server, callback=self.parse)
            yield Request(quotes_server, callback=self.parse, dont_filter=True)

        def parse(self, response):
            hits.append(response.url)

    await DSpider().start()
    assert len(hits) == 2


async def test_errback_is_called():
    errors = []

    class ESpider(Spider):
        start_urls = []
        requests_delay = 0

        def start_requests(self):
            yield Request(
                "http://127.0.0.1:1/down", callback=self.parse, errback=self.err
            )

        def parse(self, response):
            pass

        def err(self, request, ex):
            errors.append(request.url)

    spider = ESpider()
    spider.retry_policy.max_retries = 0
    await spider.start()
    assert errors == ["http://127.0.0.1:1/down"]
