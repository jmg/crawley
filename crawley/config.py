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
REQUEST_MAX_RETRIES = 3

MOZILLA_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Crawlers
MAX_CONCURRENCY = 100
"""Maximum number of in-flight requests (asyncio tasks)."""

# Scrapers
SIMILARITY_RATIO = 0.45
