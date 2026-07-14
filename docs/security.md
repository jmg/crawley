# Security & stealth

Crawling untrusted or user-supplied URLs at scale needs a few guardrails.
`crawley` ships them as opt-in features on the HTTP layer.

## SSRF protection

A crawler that follows links (or HTTP redirects) is a classic
[SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
vector: a link can point at `127.0.0.1`, a private `10.0.0.0/8` host, or the
cloud metadata endpoint `169.254.169.254` and read secrets. Enable the guard to
refuse those targets:

```python
class SafeCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    SSRF_PROTECT = True        # block private / loopback / metadata targets
```

or globally in `settings.py` (`SSRF_PROTECT = True`), or via
`crawley.config.SSRF_PROTECT`.

When enabled, an `httpx` request event-hook runs on **every request and every
redirect hop** (it only inspects the URL, so it adds no extra connection) and
rejects:

- non-HTTP(S) schemes,
- URLs with embedded `user:pass@` credentials,
- the built-in blocked host names (`localhost`, cloud-metadata aliases, …),
- any host that resolves to a private, loopback, link-local, reserved,
  multicast or unspecified address.

It is **off by default** so local-development crawls of `localhost` keep working.

The helpers are importable directly:

```python
from crawley.http import urlguard

urlguard.is_safe_url("http://169.254.169.254/")   # -> False
urlguard.assert_safe_url("https://example.com/")  # returns the url or raises UnsafeUrl
```

### Custom policy

To enforce your own policy (an allow-list, IP pinning, …), register it once at
start-up — the HTTP layer will use it everywhere the guard runs:

```python
from crawley.http import urlguard

def my_guard(url: str) -> bool:
    return url.startswith("https://api.mysite.com/")

urlguard.set_url_guard(my_guard)     # urlguard.reset_url_guard() restores the default
```

## Browser TLS/JA3 impersonation

Header-only "stealth" (spoofing the `User-Agent`) is trivially detected: anti-bot
services fingerprint the **TLS handshake (JA3)** and **HTTP/2 frame order**,
which a header doesn't change. Send a real browser fingerprint instead:

```bash
pip install "crawley[impersonate]"     # pulls in curl_cffi
```

```python
class StealthCrawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    IMPERSONATE = "chrome"       # any curl_cffi browser profile
```

When `IMPERSONATE` is set and `curl_cffi` is installed, requests use a
`curl_cffi`-backed client with a real Chrome TLS/HTTP2 fingerprint; if the
dependency is missing it falls back to `httpx` automatically. SSRF protection
(when enabled) and the response size cap apply to this path too — redirects are
followed manually so each hop is guarded.

## Proxies & proxy pools

A single proxy:

```python
class Crawler(BaseCrawler):
    PROXY_HOST = "gw.example.com"
    PROXY_PORT = 7000
    PROXY_USER = "user"          # optional
    PROXY_PASS = "pass"          # optional
```

Or a pool rotated round-robin, one proxy per request (overrides the single
proxy above) — useful to spread load across residential/rotating exits:

```python
class Crawler(BaseCrawler):
    PROXY_POOL = [
        "http://user:pass@a.proxy:7000",
        "http://user:pass@b.proxy:7000",
    ]
```

## Response size cap

Every response body is streamed and hard-stopped at
`config.MAX_RESPONSE_BYTES` (default **25 MB**), then truncated — never
discarded — so a mislabeled multi-GB body caught by a link-follow can't OOM the
process while the extractor still sees the leading HTML. Raise or lower it
globally, per project (`settings.py`), or per crawler:

```python
class Crawler(BaseCrawler):
    start_urls = ["https://example.com/"]
    # inherited from crawley.config; override in settings.py to change globally
```

```python
# settings.py
MAX_RESPONSE_BYTES = 50 * 1024 * 1024
```

## Settings summary

| Setting | Default | Purpose |
|---------|---------|---------|
| `SSRF_PROTECT` | `False` | Block private/loopback/metadata targets (every hop). |
| `IMPERSONATE` | `None` | `curl_cffi` browser profile for a real TLS/JA3 fingerprint. |
| `PROXY_HOST` / `PROXY_PORT` / `PROXY_USER` / `PROXY_PASS` | — | A single upstream proxy. |
| `PROXY_POOL` | `None` | List of proxy URLs rotated one-per-request. |
| `MAX_RESPONSE_BYTES` | `26214400` | Hard per-response body cap (streamed + truncated). |
