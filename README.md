# crawley

### A pythonic crawling / scraping framework for **Python 3**, built on `asyncio` + `httpx`.

![CI](https://github.com/jmg/crawley/actions/workflows/ci.yml/badge.svg)

`crawley` lets you crawl websites and extract structured data with a tiny,
declarative API. This is the modernized release: the legacy `eventlet` / `elixir`
stack has been replaced by **asyncio**, **httpx** and **SQLAlchemy 2.x**.

---

### Features

* High speed asynchronous crawler powered by `asyncio` + `httpx`.
* Extract data with your favourite tool: **XPath**, **CSS selectors** or
  **PyQuery** (a jQuery-like API).
* Persist to relational databases (SQLite, PostgreSQL, MySQL, Oracle) via
  SQLAlchemy 2.x, to **MongoDB** / **CouchDB**, or export to **JSON / XML / CSV**.
* Cookie handling, proxies, request delays and retries out of the box.
* A small DSL to define scrapers declaratively.
* Command line tools (`crawley startproject`, `crawley run`, ...).
* Optional visual scraping browser (PySide6).

---

### Requirements

* Python 3.9+

### Install

```bash
~$ pip install crawley            # core (httpx, lxml, pyquery, cssselect)
~$ pip install "crawley[sql]"     # + SQLAlchemy for relational storage
~$ pip install "crawley[mongo]"   # + pymongo
~$ pip install "crawley[gui]"     # + PySide6 visual browser
~$ pip install "crawley[dev]"     # tests + linters
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

## Development

```bash
~$ pip install -e ".[dev]"
~$ pytest          # run the (hermetic) test suite
~$ ruff check crawley
```

The test suite spins up a local HTTP server, so it never hits the network.

---

### License

GPL v3
