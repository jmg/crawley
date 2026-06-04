# crawley

**A pythonic crawling / scraping framework for Python 3, built on `asyncio` + `httpx`.**

crawley lets you crawl websites and extract structured data with a tiny,
declarative API. This is the modernized release: the legacy `eventlet` /
`elixir` stack has been replaced by **asyncio**, **httpx** and
**SQLAlchemy 2.x**.

## Two ways to use it

=== "As a scraping library"

    The fastest way to pull data out of a page:

    ```python
    from crawley.scraping import fetch

    doc = fetch("https://quotes.toscrape.com/")
    for quote in doc.css("div.quote"):
        print(quote.css_first("small.author").text,
              "->",
              quote.css_first("span.text").text)
    ```

    See [Scraping API](scraping.md).

=== "As a crawling framework"

    Define crawlers and scrapers declaratively and let crawley walk the site:

    ```python
    from crawley.crawlers import BaseCrawler
    from crawley.scrapers import BaseScraper

    class QuotesScraper(BaseScraper):
        matching_urls = ["%quotes.toscrape.com%"]

        def scrape(self, response):
            for q in response.css("div.quote"):
                print(q.css_first("span.text").text)

    class QuotesCrawler(BaseCrawler):
        start_urls = ["https://quotes.toscrape.com/"]
        scrapers = [QuotesScraper]
        max_depth = 2

    QuotesCrawler().run()
    ```

    See [Crawlers & Scrapers](crawler.md).

## Features

- High speed **asynchronous** crawler powered by `asyncio` + `httpx`.
- Extract data with **XPath**, **CSS selectors** or **PyQuery**.
- A modern, ergonomic [scraping API](scraping.md) (`fetch`, `Document`, `extract`).
- [Politeness](politeness.md): `robots.txt`, per-host rate limiting and
  retries with exponential backoff.
- [Persistence](persistence.md): SQL (SQLAlchemy 2.x), MongoDB, CouchDB and
  JSON / XML / CSV exports.
- A small [DSL and CLI](cli.md) (`crawley startproject`, `crawley run`, ...).

## Requirements

- Python 3.9+

Continue with the [installation guide](installation.md).
