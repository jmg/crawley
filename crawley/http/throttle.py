"""Per-host politeness: rate limiting and concurrency control.

Keeps a minimum delay between consecutive requests to the same host and,
optionally, caps how many requests run against a host at the same time.
"""

import asyncio
import time


class HostRateLimiter:
    """Throttle requests on a per-host basis."""

    def __init__(self, delay=0.0, max_per_host=None):
        self.delay = delay
        self.max_per_host = max_per_host
        self._last = {}
        self._locks = {}
        self._delays = {}
        self._sems = {}

    def set_delay(self, host, delay):
        """Override the minimum delay for a single *host* (e.g. from robots)."""
        if delay is not None:
            self._delays[host] = delay

    def _delay_for(self, host):
        return self._delays.get(host, self.delay)

    def _lock(self, host):
        return self._locks.setdefault(host, asyncio.Lock())

    def semaphore(self, host):
        """Return the per-host semaphore (or ``None`` when uncapped)."""
        if self.max_per_host is None:
            return None
        return self._sems.setdefault(host, asyncio.Semaphore(self.max_per_host))

    async def throttle(self, host):
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
