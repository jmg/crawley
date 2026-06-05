"""Per-host politeness: rate limiting and concurrency control.

Keeps a minimum delay between consecutive requests to the same host and,
optionally, caps how many requests run against a host at the same time.
"""

from __future__ import annotations

import asyncio
import time
from typing import Optional


class HostRateLimiter:
    """Throttle requests on a per-host basis."""

    def __init__(
        self, delay: float = 0.0, max_per_host: Optional[int] = None
    ) -> None:
        self.delay = delay
        self.max_per_host = max_per_host
        self._last: dict[str, float] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._delays: dict[str, float] = {}
        self._sems: dict[str, asyncio.Semaphore] = {}

    def set_delay(self, host: str, delay: Optional[float]) -> None:
        """Override the minimum delay for a single *host* (e.g. from robots)."""
        if delay is not None:
            self._delays[host] = delay

    def _delay_for(self, host: str) -> float:
        return self._delays.get(host, self.delay)

    def _lock(self, host: str) -> asyncio.Lock:
        return self._locks.setdefault(host, asyncio.Lock())

    def semaphore(self, host: str) -> Optional[asyncio.Semaphore]:
        """Return the per-host semaphore (or ``None`` when uncapped)."""
        if self.max_per_host is None:
            return None
        return self._sems.setdefault(host, asyncio.Semaphore(self.max_per_host))

    async def throttle(self, host: str) -> None:
        """Wait so that requests to *host* respect the configured delay."""
        delay = self._delay_for(host)
        if delay <= 0:
            return

        async with self._lock(host):
            last = self._last.get(host)
            now = time.monotonic()
            if last is not None:
                wait = delay - (now - last)
                if wait > 0:
                    await asyncio.sleep(wait)
            self._last[host] = time.monotonic()
