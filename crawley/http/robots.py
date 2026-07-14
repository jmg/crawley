"""``robots.txt`` support.

Fetches and caches each host's ``robots.txt`` (asynchronously, through the
crawler's own httpx client) and answers whether a url may be crawled. Also
exposes the ``Crawl-delay`` directive when present.
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class RobotsPolicy:
    """Cache and evaluate ``robots.txt`` rules per host."""

    def __init__(self, user_agent: str = "*", enabled: bool = True) -> None:
        self.user_agent = user_agent
        self.enabled = enabled
        self._cache: dict[tuple[str, str], Optional[RobotFileParser]] = {}
        self._locks: dict[tuple[str, str], asyncio.Lock] = {}

    async def allowed(self, url: str, client: Any) -> bool:
        """Return ``True`` if *url* may be fetched according to robots.txt."""
        if not self.enabled:
            return True
        parser = await self._get_parser(url, client)
        if parser is None:
            return True
        return parser.can_fetch(self.user_agent, url)

    def crawl_delay(self, url: str) -> Optional[float]:
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
    def _key(url: str) -> tuple[str, str]:
        parsed = urlparse(url)
        return (parsed.scheme, parsed.netloc)

    async def _get_parser(
        self, url: str, client: Any
    ) -> Optional[RobotFileParser]:
        key = self._key(url)
        if key in self._cache:
            return self._cache[key]

        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            if key in self._cache:
                return self._cache[key]
            try:
                parser = await self._fetch_parser(key, client)
            except Exception:
                # A TRANSIENT fetch failure (network error / timeout) must not be
                # cached: this policy lives for the whole crawl, so caching an
                # allow-all here would permanently skip robots.txt for the host
                # after one blip. Allow this request but leave the cache empty so
                # a later request re-fetches.
                fallback = RobotFileParser()
                fallback.allow_all = True  # type: ignore[attr-defined]
                return fallback
            self._cache[key] = parser
            return parser

    async def _fetch_parser(
        self, key: tuple[str, str], client: Any
    ) -> RobotFileParser:
        scheme, netloc = key
        robots_url = "%s://%s/robots.txt" % (scheme, netloc)
        parser = RobotFileParser()

        # A network error propagates to _get_parser, which declines to cache it.
        response = await client.get(robots_url)

        # These are DEFINITIVE outcomes and safe to cache for the crawl.
        if response.status_code in (401, 403):
            parser.disallow_all = True  # type: ignore[attr-defined]
        elif response.status_code >= 400:
            parser.allow_all = True  # type: ignore[attr-defined]
        else:
            parser.parse(response.text.splitlines())
        return parser
