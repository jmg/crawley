"""Example 6 — the callback-driven Spider with an item pipeline.

`parse` extracts quotes and follows the pagination link; an item pipeline
normalizes each item before it reaches `on_item`.

Run it::

    python examples/06_spider.py
"""

from crawley.pipelines import DropItem, ItemPipeline
from crawley.spider import Spider

LIVE_SITE = "https://quotes.toscrape.com/"


class CleanPipeline(ItemPipeline):
    def process_item(self, item, spider):
        item["text"] = item["text"].strip().strip("“”\"")
        if not item["text"]:
            raise DropItem("empty quote")
        return item


def crawl_quotes(base_url=LIVE_SITE):
    """Crawl all pages following pagination and return the cleaned items."""
    collected = []

    class QuotesSpider(Spider):
        name = "quotes"
        start_urls = [base_url]
        pipelines = [CleanPipeline]
        requests_delay = 0
        requests_deviation = 0

        def parse(self, response):
            for quote in response.css("div.quote"):
                yield {
                    "text": quote.css_first("span.text").text,
                    "author": quote.css_first("small.author").text,
                    "page": response.meta.get("depth", 0) + 1,
                }
            nxt = response.css_first("li.next a")
            if nxt:
                yield response.follow(nxt.attr("href"))

        def on_item(self, item):
            collected.append(item)

    QuotesSpider().run()
    return collected


if __name__ == "__main__":
    items = crawl_quotes()
    print(f"Collected {len(items)} quotes across {max(i['page'] for i in items)} pages")
    for item in items[:5]:
        print(f"- {item['author']}: {item['text']}")
