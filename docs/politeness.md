# Politeness — robots, rate limiting, retries

crawley ships the building blocks to crawl responsibly and robustly: it can
honour `robots.txt`, throttle requests per host and retry transient failures
with exponential backoff.

## robots.txt

Set `respect_robots = True` to make the crawler fetch and obey each host's
`robots.txt`:

```python
class MyCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    respect_robots = True
```

- Each host's `robots.txt` is fetched once and cached.
- Disallowed urls are skipped and `on_robots_blocked(url)` is called.
- A `404` robots.txt allows everything; a `401`/`403` disallows everything.
- A `Crawl-delay` directive is automatically applied as the per-host delay.

```python
class MyCrawler(BaseCrawler):
    respect_robots = True

    def on_robots_blocked(self, url):
        print("skipped (robots):", url)
```

You can use the policy on its own too:

```python
import httpx
from crawley.http.robots import RobotsPolicy

policy = RobotsPolicy(user_agent="my-bot")
async with httpx.AsyncClient() as client:
    await policy.allowed("https://example.com/private", client)  # -> bool
```

## Per-host rate limiting

Two knobs control how hard a single host is hit:

```python
class MyCrawler(BaseCrawler):
    crawl_delay = 1.0                 # >= 1s between requests to the same host
    max_concurrency_per_host = 2      # at most 2 concurrent requests per host
```

`crawl_delay` enforces a minimum spacing between consecutive requests to the
same host, while `max_concurrency_level` still bounds the *global* number of
in-flight requests. Different hosts are throttled independently.

The underlying primitive is `crawley.http.throttle.HostRateLimiter`.

## Retries with backoff

Failed requests — network errors and retryable HTTP statuses such as
`429`, `500`, `502`, `503`, `504` — are retried automatically:

```python
class MyCrawler(BaseCrawler):
    max_retries = 3                   # attempts after the first failure
    retry_backoff = 0.5               # base seconds for the backoff
    retry_statuses = {429, 503}       # which statuses to retry
```

- Backoff is exponential with jitter: roughly
  `retry_backoff * 2 ** attempt`, capped at 30s.
- A `Retry-After` response header (seconds or HTTP date) takes precedence.
- After exhausting the retries, the last response is returned (so you can
  inspect a final `503`); persistent network errors are re-raised and routed
  to `on_request_error`.

The policy is `crawley.http.retry.RetryPolicy` and can be used standalone:

```python
from crawley.http.retry import RetryPolicy

policy = RetryPolicy(max_retries=5, backoff_factor=0.5, statuses={503})
policy.should_retry(attempt=0, response=resp)   # -> bool
policy.backoff_time(attempt=2)                  # -> seconds
```

## Putting it together

```python
class PoliteCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    respect_robots = True
    crawl_delay = 1.0
    max_concurrency_per_host = 2
    max_retries = 3
    retry_backoff = 0.5
```
