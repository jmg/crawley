# Crawlers & Scrapers

A **crawler** walks a site starting from `start_urls`, and delegates data
extraction to one or more **scrapers**.

## A minimal crawler

```python
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor


class QuotesScraper(BaseScraper):
    # only pages matching these patterns are scraped ("%" is a wildcard)
    matching_urls = ["%quotes.toscrape.com%"]

    def scrape(self, response):
        for quote in response.css("div.quote"):
            print(quote.css_first("span.text").text)


class QuotesCrawler(BaseCrawler):
    start_urls = ["https://quotes.toscrape.com/"]
    scrapers = [QuotesScraper]
    max_depth = 2
    extractor = XPathExtractor      # or CSSExtractor / PyQueryExtractor


QuotesCrawler().run()               # synchronous entry point
# await QuotesCrawler().start()     # ...or from your own event loop
```

`run()` is a convenience wrapper around `asyncio.run(self.start())`.

## Crawler options

| Attribute                  | Default          | Description                                        |
|----------------------------|------------------|----------------------------------------------------|
| `start_urls`               | `[]`             | Where the crawl begins.                            |
| `scrapers`                 | `[]`             | Scraper classes to run on each page.               |
| `max_depth`                | `-1`             | Recursion depth (`-1` = unlimited).                |
| `allowed_urls`             | `[]`             | Only crawl urls matching these patterns.           |
| `black_list`               | `[]`             | Never crawl urls matching these patterns.          |
| `extractor`                | `XPathExtractor` | How `response.html` is parsed.                     |
| `max_concurrency_level`    | `100`            | Max in-flight requests.                            |
| `requests_delay`           | `0.5`            | Average delay between requests (s).                |
| `requests_deviation`       | `0.25`           | Random jitter on the delay (s).                    |
| `search_all_urls`          | `True`           | Follow links found on the page.                    |
| `search_hidden_urls`       | `False`          | Also discover urls via a regex over the html.      |
| `unique_urls`              | `True`           | Skip already-visited urls (prevents loops).        |
| `post_urls`                | `[]`             | `(pattern, data)` tuples to issue POSTs.           |
| `login`                    | `None`           | `(url, data)` to authenticate before crawling.     |
| `unique_urls`              | `True`           | Skip already-visited urls.                         |
| `http_cache`               | `False`          | Cache responses on disk (development helper).      |
| `http_cache_dir`           | `.crawley_cache` | Where the HTTP cache is stored.                    |
| `render_js`                | `False`          | Render pages with Playwright (`crawley[js]`).      |

See [Politeness](politeness.md) for `respect_robots`, `crawl_delay`,
`max_concurrency_per_host` and the retry options.

## Stats

Every crawler / spider owns a `stats` collector. It counts requests, responses,
per-status codes, errors, robots blocks, items (spiders) and the elapsed time,
and logs a summary when the crawl finishes:

```python
crawler = MyCrawler()
crawler.run()
print(crawler.stats.get_stats())
# {'requests': 12, 'responses': 12, 'status/200': 12, 'elapsed_seconds': 1.3, ...}
```

## HTTP cache (development)

Set `http_cache = True` to cache every response on disk (keyed by
method + url + body). Re-running the crawl then serves from the cache instead of
hitting the site again — handy while developing scrapers:

```python
class MyCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    http_cache = True
    http_cache_dir = ".crawley_cache"
```

## URL matching

Patterns use `%` as a wildcard:

| Pattern        | Matches                          |
|----------------|----------------------------------|
| `"%foo%"`      | `foo` anywhere in the url        |
| `"foo%"`       | url starts with `foo`            |
| `"%foo"`       | url ends with `foo`              |
| `"foo"`        | exact match                      |

## Extractors

`response.html` is produced by the crawler's `extractor`:

| Extractor          | `response.html` is...   | Query with                    |
|--------------------|-------------------------|-------------------------------|
| `XPathExtractor`   | an `lxml` tree          | `.xpath(...)`                 |
| `CSSExtractor`     | an `lxml` tree          | `.getroot().cssselect(...)`   |
| `PyQueryExtractor` | a `PyQuery` object      | `pq("div.foo")`               |
| `RawExtractor`     | the raw html `str`      | anything                      |

Regardless of the extractor, the modern shortcuts (`response.css`,
`response.css_first`, `response.extract`, `response.doc`) are always available.

## Events

Override these hooks to react to the crawl lifecycle:

```python
class MyCrawler(BaseCrawler):
    def on_start(self): ...
    def on_finish(self): ...
    def on_request_error(self, url, ex): ...
    def on_robots_blocked(self, url): ...
```

## POST requests and login

```python
class MyCrawler(BaseCrawler):
    start_urls = ["https://site/search"]
    post_urls = [("%/search%", {"q": "crawley"})]
    login = ("https://site/login", {"user": "me", "password": "secret"})
```

## Specialized crawlers

- **`FastCrawler`** — issues requests without the per-request delay.
- **`OffLineCrawler`** — rewrites relative `link`/`img` urls to absolute ones
  so saved pages render offline.

## SmartScraper

`SmartScraper` only scrapes pages whose html **structure** is similar to a
template page, which is handy when a site has many pages sharing a layout:

```python
from crawley.scrapers import SmartScraper

class ProductScraper(SmartScraper):
    matching_urls = ["%/product/%"]
    template_url = "https://shop.example/product/1"
    ratio = 0.45     # similarity threshold

    def scrape(self, response):
        ...
```
