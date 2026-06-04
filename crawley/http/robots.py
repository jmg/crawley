"""``robots.txt`` support.

Fetches and caches each host's ``robots.txt`` (asynchronously, through the
crawler's own httpx client) and answers whether a url may be crawled. Also
exposes the ``Crawl-delay`` directive when present.
"""

import asyncio
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class RobotsPolicy:
    """Cache and evaluate ``robots.txt`` rules per host."""

    def __init__(self, user_agent="*", enabled=True):
        self.user_agent = user_agent
        self.enabled = enabled
        self._cache = {}
        self._locks = {}

    async def allowed(self, url, client):
        """Return ``True`` if *url* may be fetched according to robots.txt."""
        if not self.enabled:
            return True
        parser = await self._get_parser(url, client)
        if parser is None:
            return True
        return parser.can_fetch(self.user_agent, url)

    def crawl_delay(self, url):
        """Return the ``Crawl-delay`` for *url*'s host, if any."""
        parser = self._cache.get(self._key(url))
        if parser is None:
            return None
        try:
            value = parser.crawl_delay(self.user_agent)
        except AttributeError:  # pragma: no cover - older stdlib
            return None
        return float(value) if value is not None else None

    @staticmethod
    def _key(url):
        parsed = urlparse(url)
        return (parsed.scheme, parsed.netloc)

    async def _get_parser(self, url, client):
        key = self._key(url)
        if key in self._cache:
            return self._cache[key]

        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            if key in self._cache:
                return self._cache[key]
            parser = await self._fetch_parser(key, client)
            self._cache[key] = parser
            return parser

    async def _fetch_parser(self, key, client):
        scheme, netloc = key
        robots_url = "%s://%s/robots.txt" % (scheme, netloc)
        parser = RobotFileParser()

        try:
            response = await client.get(robots_url)
        except Exception:
            # If robots.txt can't be fetched, default to allowing the crawl.
            parser.allow_all = True
            return parser

        if response.status_code in (401, 403):
            parser.disallow_all = True
        elif response.status_code >= 400:
            parser.allow_all = True
        else:
            parser.parse(response.text.splitlines())
        return parser
