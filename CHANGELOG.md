# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/).

## [0.3.0] — Python 3 modernization

A full port of the legacy Python 2 framework to a modern Python 3 (3.9+) stack.

### Added
- **Modern scraping API** (`crawley.scraping`): `fetch` / `afetch` /
  `afetch_all` / `scrape` / `parse` and `Document` / `Element` with CSS
  selectors (`::text`, `::attr(name)` pseudo-suffixes), XPath, `links()` and
  declarative `extract()`. The same shortcuts (`css`, `css_first`, `extract`,
  `doc`) are available on the crawler's `response`.
- **CSSExtractor** for CSS-selector based extraction.
- **Politeness**: opt-in `robots.txt` support (`respect_robots`,
  `on_robots_blocked`, `Crawl-delay`), per-host rate limiting (`crawl_delay`,
  `max_concurrency_per_host`) and a configurable `RetryPolicy` with exponential
  backoff, jitter and `Retry-After` support (`max_retries`, `retry_backoff`,
  `retry_statuses`).
- **Visited-url de-duplication** (`unique_urls`) preventing redundant fetches
  and crawl loops.
- **Callback-driven `Spider`** (`crawley.spider`): `Request` with
  callback / `meta` / `cb_kwargs` / `errback`, `response.follow()`, `Item`, and
  fingerprint-based de-duplication — for list→detail crawls.
- **Item pipelines** (`crawley.pipelines`): `ItemPipeline` + `DropItem`.
- **`CrawlSpider`** with `Rule` / `LinkExtractor` (allow/deny/restrict) and
  **`SitemapSpider`** (`crawley.spiders`).
- **JavaScript rendering** via Playwright (`render_js = True`, extra
  `crawley[js]`).
- Documentation site (MkDocs Material + mkdocstrings) and a set of runnable,
  test-covered `examples/`.
- **Type hints** on the public modules and a PEP 561 `py.typed` marker so
  downstream code gets type information; `mypy` runs in CI.
- A `LICENSE` file (GPL-3.0).
- A hermetic `pytest` suite (~185 tests, ~90% core coverage).

### Changed
- Concurrency moved from `eventlet` green pools to **asyncio** (`AsyncPool`);
  crawlers are coroutines with a synchronous `run()` wrapper.
- HTTP layer rebuilt on **httpx** (`AsyncClient`): cookies, proxies, timeouts.
- Relational persistence migrated from `elixir` + SQLAlchemy 0.7.8 to
  **SQLAlchemy 2.x**; MongoDB on current `pymongo`; CouchDB via a small httpx
  client.
- GUI ported from PyQt4/QtWebKit to **PySide6/QtWebEngine** (optional extra).
- Packaging moved to **`pyproject.toml`** (PEP 621) with optional extras
  (`sql`, `mongo`, `gui`, `shell`, `http2`, `dev`, `docs`) and a `crawley`
  console script.
- CI moved from Travis to **GitHub Actions** (Python 3.9–3.12, ruff + pytest).
- Logging is used instead of `print`; the `crawley` logger ships a
  `NullHandler`.

### Removed
- The `eventlet`, `elixir` and legacy SQLAlchemy 0.7.8 dependencies.
- `setup.py` / `setup.cfg` / `requirements.txt` / `.travis.yml` and the old
  Sphinx `doc/` tree.

## [0.2.5]
- Last Python 2 release.
