# Spiders (callbacks, items & pipelines)

Besides the `BaseCrawler` + `BaseScraper` model, crawley ships a more powerful,
Scrapy-style **Spider** built on the same async engine (httpx, retries, rate
limiting, robots.txt, de-duplication).

## Requests with callbacks

A `Spider` defines `parse()` (the default callback) and yields `Request`
objects — or `response.follow(...)` — to crawl further, and dicts / `Item`
objects to emit data.

```python
from crawley.spider import Spider

class BlogSpider(Spider):
    name = "blog"
    start_urls = ["https://example.com/blog/"]

    def parse(self, response):
        # follow each post to a detail callback
        for href in response.css("a.post::attr(href)"):
            yield response.follow(href, callback=self.parse_post)
        # follow pagination with the default callback (parse)
        nxt = response.css_first("a.next::attr(href)")
        if nxt:
            yield response.follow(nxt)

    def parse_post(self, response):
        yield {
            "title": response.css_first("h1").text,
            "url": response.url,
        }

BlogSpider().run()          # or: await BlogSpider().start()
```

### Passing state: `meta` and `cb_kwargs`

```python
def parse(self, response):
    yield response.follow(
        "/item/1",
        callback=self.parse_item,
        meta={"category": "books"},     # available as response.meta
        cb_kwargs={"rank": 1},          # passed as a keyword argument
    )

def parse_item(self, response, rank=None):
    yield {"category": response.meta["category"], "rank": rank}
```

`Request` supports `method`, `data` (POST), `headers`, `priority`,
`dont_filter` (bypass de-duplication) and `errback` (per-request error
handler). De-duplication uses a fingerprint of *method + url + body*.

## Item pipelines

Pipelines post-process every emitted item in order. Raise `DropItem` to discard
one.

```python
from crawley.pipelines import ItemPipeline, DropItem

class PricePipeline(ItemPipeline):
    def open_spider(self, spider): ...
    def close_spider(self, spider): ...

    def process_item(self, item, spider):
        if not item.get("price"):
            raise DropItem("missing price")
        item["price"] = float(item["price"])
        return item            # may be sync or async

class ShopSpider(Spider):
    pipelines = [PricePipeline]
    ...
```

Items that survive the pipeline reach `on_item(item)` (override it, or use a
pipeline, to store them — e.g. with the [persistence](persistence.md) layer).

## Rule-based crawling: `CrawlSpider`

`CrawlSpider` follows links automatically according to a list of `Rule`s, each
built from a `LinkExtractor`.

```python
from crawley.spiders import CrawlSpider, Rule, LinkExtractor

class SiteSpider(CrawlSpider):
    start_urls = ["https://books.example/"]
    rules = [
        # paginate, just follow
        Rule(LinkExtractor(allow=[r"/catalogue/page-\d+"])),
        # product pages -> extract with parse_book
        Rule(LinkExtractor(allow=[r"/catalogue/.+/index\.html"]),
             callback="parse_book"),
    ]

    def parse_book(self, response):
        yield {"title": response.css_first("h1").text}
```

`LinkExtractor(allow, deny, restrict_xpaths, restrict_css, tags, attrs, unique)`
returns absolute, filtered links (`allow`/`deny` are regexes).

## Sitemaps: `SitemapSpider`

Seed the crawl from one or more `sitemap.xml` files (sitemap indexes are
followed automatically):

```python
from crawley.spiders import SitemapSpider

class NewsSpider(SitemapSpider):
    sitemap_urls = ["https://news.example/sitemap.xml"]

    def parse(self, response):
        yield {"title": response.css_first("h1").text, "url": response.url}
```

## JavaScript rendering

For client-side rendered / SPA sites, render pages with a headless browser
(Playwright). Install the extra and the browser, then set `render_js = True`:

```bash
pip install "crawley[js]"
playwright install chromium
```

```python
class SpaSpider(Spider):
    start_urls = ["https://app.example/"]
    render_js = True
    playwright_options = {"browser_type": "chromium", "wait_for": "div.loaded"}

    def parse(self, response):
        yield {"title": response.css_first("h1").text}
```

Everything else (selectors, `follow`, pipelines, rules, rate limiting, retries)
works the same — only the download step changes.
