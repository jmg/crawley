"""Crawley configuration defaults.

These values are module level constants used as fall-backs all over the
framework. They can be overridden per crawler (via class attributes) or per
project (via the ``settings.py`` file).
"""

# Paths
CRAWLEY_ROOT_DIR = "crawley"

# Requests
REQUEST_TIMEOUT = 30.0  # in seconds, ``None`` disables the timeout
REQUEST_DELAY = 0.5  # average delay between requests, in seconds
REQUEST_DEVIATION = 0.25  # random deviation applied to the delay, in seconds

# Hard cap on a single response body read into memory. A crawl (esp. a link_css
# follow) can hit a media file / tarball / mislabeled multi-GB page; without a
# cap that body OOM-kills the box. The GET path streams and stops reading past
# this. 25 MB is generous for any real HTML page.
MAX_RESPONSE_BYTES = 25 * 1024 * 1024

MOZILLA_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Retries / backoff
REQUEST_MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5  # base seconds; backoff = factor * 2 ** attempt
RETRY_MAX_BACKOFF = 30.0  # cap, in seconds
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
"""HTTP status codes that trigger a retry."""

# Security
SSRF_PROTECT = False
"""When ``True`` the HTTP layer blocks requests to private / loopback / link-local
/ reserved addresses and the cloud metadata endpoint — on every request *and each
redirect hop*. Off by default so local-dev crawls of ``localhost`` keep working;
enable it globally here, per crawler (a ``SSRF_PROTECT`` class attribute), or per
project (in ``settings.py``). See :mod:`crawley.http.urlguard`."""

# Stealth
IMPERSONATE = None
"""When set to a ``curl_cffi`` browser profile (e.g. ``"chrome"``) *and* the
optional ``curl_cffi`` dependency is installed (``pip install crawley[impersonate]``),
requests use a real browser TLS/JA3 + HTTP/2 fingerprint instead of vanilla
``httpx``. Usually set per crawler. See :mod:`crawley.http.impersonate`."""

PROXY_POOL = None
"""An optional list of proxy URLs rotated round-robin, one per request. Overrides
the single ``PROXY_HOST`` / ``PROXY_PORT`` proxy when set. Usually set per
crawler / project rather than here."""

# Politeness
RESPECT_ROBOTS = False
"""When ``True`` the crawler honours each site's ``robots.txt``."""

CRAWL_DELAY = 0.0
"""Minimum seconds between two requests to the same host (0 disables it)."""

MAX_CONCURRENCY_PER_HOST = None
"""Maximum simultaneous requests per host (``None`` disables the limit)."""

# Crawlers
MAX_CONCURRENCY = 100
"""Maximum number of in-flight requests (asyncio tasks)."""

# Scrapers
SIMILARITY_RATIO = 0.45
