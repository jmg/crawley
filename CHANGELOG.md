# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/).

## [0.4.0] — Security & robustness hardening

Hardens the HTTP layer for untrusted, at-scale crawling and makes the
security features self-contained (no host-application dependency).

### Added
- **SSRF protection** (`crawley.http.urlguard`): opt-in guard
  (`SSRF_PROTECT = True`, per crawler / project / global config) that blocks
  requests — and every redirect hop — to private, loopback, link-local,
  reserved and cloud-metadata (`169.254.169.254`) targets, plus non-HTTP
  schemes and `user:pass@` URLs. `is_safe_url` / `assert_safe_url` /
  `host_is_obviously_internal` are exposed, and a host app can install its own
  policy with `set_url_guard(...)`. Off by default so local-dev crawls keep
  working.
- **Browser TLS/JA3 impersonation** (`crawley.http.impersonate`): set
  `IMPERSONATE = "chrome"` (and `pip install crawley[impersonate]`) to send a
  real browser TLS + HTTP/2 fingerprint via `curl_cffi` instead of vanilla
  `httpx`, defeating handshake-fingerprint anti-bot checks. Redirects are
  followed manually so each hop is SSRF-checked, and the body is size-capped.
- **Per-request proxy-pool rotation** (`PROXY_POOL`): a list of proxy URLs
  rotated round-robin, one per request (overrides the single `PROXY_*` proxy).
- **Response body size cap** (`MAX_RESPONSE_BYTES`, default 25 MB): responses
  are streamed and truncated so a huge/mislabeled body (a media file caught by
  a link-follow) can't OOM the process — now enforced on GET, POST and the
  impersonation path alike.

### Fixed
- **Response cap escapes**: POST responses and the `curl_cffi` impersonation
  client bypassed `MAX_RESPONSE_BYTES` entirely; and a body whose
  `Content-Length` exceeded the cap was *discarded* (an empty `200` that then
  got cached), instead of truncated. All paths now stream-and-truncate.
- **`Retry-After` HTTP-date**: a date parsed to a naive datetime (e.g. a
  `-0000` zone) was compared against local wall-clock, mis-computing the wait
  by the worker's UTC offset; naive dates are now read as UTC.
- **Retry backoff overflow**: `2 ** attempt` raised `OverflowError` at very
  high attempt counts; the exponent is clamped (the delay is capped anyway).
- **URL discovery**: fragments are stripped (`page#a` / `page#b` were treated
  as distinct pages, defeating de-dup) and non-web links
  (`mailto:` / `javascript:` / `tel:` / `data:`) are dropped instead of being
  enqueued and fetched.
- **Cookie jar**: a truncated/corrupt persisted jar (a crawl killed mid-save)
  raised `LoadError` and crashed request-manager construction; it is now
  ignored (start with a fresh jar).
- **`robots.txt` caching**: a transient fetch failure cached an allow-all
  verdict for the whole crawl; only definitive results are cached now, so a
  blip is retried.
- **Spider error handling**: exceptions in a user `parse()` / pipeline /
  `on_item` were swallowed by the task pool (item silently lost) — they are now
  counted (`callback_errors`), logged and routed to the errback; and an
  `async def` errback is now awaited instead of being left as an un-run
  coroutine.
- **AutoThrottle**: the `enabled=False` switch was ignored (it still adapted
  and mutated state); it now returns a fixed delay.
- **Gzipped sitemaps**: a `.xml.gz` sitemap served as `application/gzip` is now
  transparently decompressed before parsing.
- **HTTP cache**: transient error responses (4xx/5xx) were cached and replayed
  on every later run (the cache has no TTL); only success/redirect responses
  are cached now.

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
- **Stats collector** (`crawley.stats.StatsCollector`): per-crawl counters
  (requests/responses/status/errors/items/elapsed), logged on finish.
- **On-disk HTTP cache** (`http_cache = True`) for development.
- **`FormRequest.from_response`** to pre-fill and submit forms.
- **Downloader middlewares** (`crawley.middlewares.DownloaderMiddleware`):
  `process_request` / `process_response` / `process_exception` chains on the
  `Spider` (sync or async).
- **AutoThrottle** (`autothrottle = True`): adapt the per-host delay to the
  observed response latency.
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
