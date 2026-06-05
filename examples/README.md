# Examples

Runnable, documented examples. Each one targets
[`quotes.toscrape.com`](https://quotes.toscrape.com/) by default but takes a
`base_url` argument, so the test suite runs them against a local server too.

| File | Shows |
|------|-------|
| [`01_scraping_quickstart.py`](01_scraping_quickstart.py) | The high-level scraping API: `fetch`, CSS/XPath selectors, declarative `extract`. |
| [`02_crawler.py`](02_crawler.py) | A `BaseCrawler` + `BaseScraper` that follows pagination. |
| [`03_polite_crawler.py`](03_polite_crawler.py) | Politeness: `robots.txt`, per-host rate limiting and retries. |
| [`04_persistence_json.py`](04_persistence_json.py) | Persisting scraped data to a JSON document. |
| [`05_concurrent_fetch.py`](05_concurrent_fetch.py) | Fetching many pages concurrently with `afetch_all`. |
| [`06_spider.py`](06_spider.py) | The callback-driven `Spider` with an item pipeline. |

Run any of them with:

```bash
python examples/01_scraping_quickstart.py
```

The `*/` project directories (`ebay/`, `pypi_crawler/`, ...) are legacy
`crawley startproject` layouts kept for reference; see the
[CLI docs](../docs/cli.md) for the current project workflow.
