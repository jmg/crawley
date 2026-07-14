# crawley

### A pythonic crawling / scraping framework for **Python 3**, built on `asyncio` + `httpx`.

![CI](https://github.com/jmg/crawley/actions/workflows/ci.yml/badge.svg)

`crawley` lets you crawl websites and extract structured data with a tiny,
declarative API. This is the modernized release: the legacy `eventlet` / `elixir`
stack has been replaced by **asyncio**, **httpx** and **SQLAlchemy 2.x**.

📖 **Documentation:** <https://jmg.github.io/crawley/> — or run `mkdocs serve`
locally (see [Development](#development)).

---

### Features

* High speed asynchronous crawler powered by `asyncio` + `httpx`.
* A modern, ergonomic **scraping API** (`fetch`, `Document`, CSS/XPath, `extract`).
* Extract data with your favourite tool: **XPath**, **CSS selectors** or
  **PyQuery** (a jQuery-like API).
* **Politeness** built in: `robots.txt`, per-host rate limiting and retries with
  exponential backoff.
* **Security & stealth**: opt-in [SSRF protection](docs/security.md) (blocks
  private/loopback/metadata targets on every redirect hop), a per-response size
  cap, and optional real-browser TLS/JA3 [impersonation](docs/security.md).
* Persist to relational databases (SQLite, PostgreSQL, MySQL, Oracle) via
  SQLAlchemy 2.x, to **MongoDB** / **CouchDB**, or export to **JSON / XML / CSV**.
* Cookie handling, single proxies and rotating **proxy pools** out of the box.
* A small DSL to define scrapers declaratively.
* Command line tools (`crawley startproject`, `crawley run`, ...).
* Optional visual scraping browser (PySide6).

---

### Requirements

* Python 3.9+

### Install

```bash
~$ pip install crawley                # core (httpx, lxml, pyquery, cssselect)
~$ pip install "crawley[sql]"         # + SQLAlchemy for relational storage
~$ pip install "crawley[mongo]"       # + pymongo
~$ pip install "crawley[gui]"         # + PySide6 visual browser
~$ pip install "crawley[impersonate]" # + curl_cffi for browser TLS/JA3 stealth
~$ pip install "crawley[dev]"         # tests + linters
```

From a checkout:

```bash
~$ pip install -e ".[dev]"
```

---

## Quick start (as a library)

```python
import asyncio
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor


class QuotesScraper(BaseScraper):
    # only pages matching these patterns are scraped ("%" is a wildcard)
    matching_urls = ["%quotes.toscrape.com%"]

    def scrape(self, response):
        for quote in response.html.xpath("//div[@class='quote']"):
            text = quote.xpath(".//span[@class='text']")[0].text
            author = quote.xpath(".//small[@class='author']")[0].text
            print(author, "->", text)


class QuotesCrawler(BaseCrawler):
    start_urls = ["https://quotes.toscrape.com/"]
    scrapers = [QuotesScraper]
    max_depth = 2
    extractor = XPathExtractor      # or CSSExtractor / PyQueryExtractor


# Synchronous entry point:
QuotesCrawler().run()

# ...or await it from your own event loop:
# asyncio.run(QuotesCrawler().start())
```

Need a one-off request?

```python
from crawley.toolbox import request

response = request("https://example.com")
print(response.status_code, response.html.xpath("//title")[0].text)
```

---

## Modern scraping API (`crawley.scraping`)

For "just scrape this page" use cases there's a small, ergonomic API
(à la `parsel` / `requests-html`) built on the same `httpx` + `lxml` stack.
Selectors accept an optional `::text` or `::attr(name)` suffix.

```python
from crawley.scraping import fetch

doc = fetch("https://quotes.toscrape.com/")

doc.title                       # -> "Quotes to Scrape"
doc.css_first("h1").text        # first match (an Element)
doc.css("span.text::text")      # list of texts
doc.css("a::attr(href)")        # list of (absolute) hrefs
doc.links()                     # de-duplicated absolute links

# Declarative extraction: a string selector -> one value, [selector] -> a list
doc.extract({
    "quote":  "span.text::text",
    "author": "small.author::text",
    "tags":   ["a.tag::text"],
})
```

Fetch many pages concurrently, or scrape an url in one call:

```python
import asyncio
from crawley.scraping import afetch_all, scrape

scrape("https://example.com", {"title": "h1::text"})

docs = asyncio.run(afetch_all(["https://a.com", "https://b.com"]))
```

The same shortcuts (`response.css`, `response.css_first`, `response.extract`,
`response.doc`) are available on the crawler's `response` object inside
`scrape()`.

---

## Spiders (callbacks, items, rules, JS)

For full crawls there's a Scrapy-style `Spider`: yield `Request`s (or
`response.follow(...)`) to navigate and dicts/`Item`s to emit data, with item
pipelines, rule-based crawling and optional JavaScript rendering. See
[`docs/spiders.md`](docs/spiders.md).

```python
from crawley.spider import Spider

class BlogSpider(Spider):
    start_urls = ["https://example.com/blog/"]

    def parse(self, response):                       # default callback
        for href in response.css("a.post::attr(href)"):
            yield response.follow(href, callback=self.parse_post)
        nxt = response.css_first("a.next::attr(href)")
        if nxt:
            yield response.follow(nxt)               # follows pagination

    def parse_post(self, response):
        yield {"title": response.css_first("h1").text, "url": response.url}

BlogSpider().run()
```

- **Item pipelines**: `crawley.pipelines.ItemPipeline` + `DropItem`.
- **Rule-based**: `CrawlSpider` + `Rule(LinkExtractor(allow=..., deny=...))`.
- **Sitemaps**: `SitemapSpider(sitemap_urls=[...])`.
- **JavaScript**: `render_js = True` (install `crawley[js]` + `playwright install`).

---

## Quick start (as a framework / CLI)

### 1. Start a new project

```bash
~$ crawley startproject myproject
~$ cd myproject
```

### 2. Write your models (`myproject/models.py`)

```python
from crawley.persistance import Entity, UrlEntity, Field, Unicode

class Package(Entity):
    updated = Field(Unicode(255))
    package = Field(Unicode(255))
    description = Field(Unicode(255))
```

### 3. Write your scrapers (`myproject/crawlers.py`)

```python
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class pypiScraper(BaseScraper):
    matching_urls = ["%"]

    def scrape(self, response):
        for tr in response.html.xpath("//table/tr"):
            Package(package=tr[1].text, description=tr[2].text)

class pypiCrawler(BaseCrawler):
    start_urls = ["https://pypi.org/"]
    scrapers = [pypiScraper]
    max_depth = 0
    extractor = XPathExtractor
```

### 4. Configure `settings.py` and run

```bash
~$ crawley run
```

Other commands: `crawley syncdb`, `crawley migratedb`, `crawley shell <url>`,
`crawley browser <url>`.

---

## Extractors

| Extractor             | `response.html` is...                     | Query with            |
|-----------------------|-------------------------------------------|-----------------------|
| `XPathExtractor`      | an `lxml` tree                            | `.xpath(...)`         |
| `CSSExtractor`        | an `lxml` tree                            | `.getroot().cssselect(...)` |
| `PyQueryExtractor`    | a `PyQuery` object                        | `pq("div.foo")`       |
| `RawExtractor`        | the raw html `str`                        | anything you like     |

---

## Politeness

Crawl responsibly with a few class attributes (see
[`docs/politeness.md`](docs/politeness.md)):

```python
class PoliteCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    respect_robots = True             # honour robots.txt (+ Crawl-delay)
    crawl_delay = 1.0                 # >= 1s between requests to the same host
    max_concurrency_per_host = 2      # at most 2 concurrent requests per host
    max_retries = 3                   # retry 429/5xx + network errors...
    retry_backoff = 0.5               # ...with exponential backoff + jitter
```

Retries honour the `Retry-After` header, and `on_robots_blocked(url)` lets you
react to disallowed urls.

---

## Security & stealth

For crawling untrusted or user-supplied URLs — see [`docs/security.md`](docs/security.md):

```python
class Crawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    SSRF_PROTECT = True                 # block private/loopback/metadata (every redirect hop)
    IMPERSONATE = "chrome"              # real browser TLS/JA3 fingerprint (needs crawley[impersonate])
    PROXY_POOL = ["http://a:1", "http://b:2"]   # rotated one-per-request
```

- **SSRF guard** — `crawley.http.urlguard` (`is_safe_url` / `set_url_guard`), off
  by default, applied on every request and redirect hop when enabled.
- **Impersonation** — `crawley.http.impersonate` via `curl_cffi`; falls back to
  `httpx` if not installed.
- **Response size cap** — `MAX_RESPONSE_BYTES` (default 25 MB) streamed +
  truncated so an oversized body can't OOM the process.

---

## Development

```bash
~$ pip install -e ".[dev]"
~$ pytest          # run the (hermetic) test suite
~$ ruff check crawley
~$ pip install -e ".[docs]" && mkdocs serve   # docs preview
```

The test suite spins up a local HTTP server, so it never hits the network.

---

## Examples

Runnable, documented scripts live in [`examples/`](examples/):

| File | Shows |
|------|-------|
| `01_scraping_quickstart.py` | The scraping API: `fetch`, CSS/XPath, `extract`. |
| `02_crawler.py` | A crawler that follows pagination. |
| `03_polite_crawler.py` | `robots.txt`, rate limiting and retries. |
| `04_persistence_json.py` | Persisting scraped data to JSON. |
| `05_concurrent_fetch.py` | Concurrent fetching with `afetch_all`. |

```bash
~$ python examples/01_scraping_quickstart.py
```

Every example is exercised by the test suite against a local server, so they
stay in sync with the code.

---

### License

GPL v3
