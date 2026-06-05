"""A simple stats collector for a crawl.

Counts requests, responses, items, errors, etc. and the elapsed time. Every
crawler / spider owns one as ``self.stats`` and logs a summary when it finishes.
"""

from __future__ import annotations

import time
from typing import Any, Optional


class StatsCollector:
    """Collect counters and values during a crawl."""

    def __init__(self) -> None:
        self._stats: dict[str, Any] = {}
        self._start: Optional[float] = None

    def open(self) -> None:
        """Reset the stats and start the clock."""
        self._stats = {}
        self._start = time.monotonic()

    def close(self) -> None:
        """Record the total elapsed time."""
        if self._start is not None:
            self.set("elapsed_seconds", round(time.monotonic() - self._start, 3))

    def inc(self, key: str, count: int = 1) -> None:
        self._stats[key] = self._stats.get(key, 0) + count

    def set(self, key: str, value: Any) -> None:
        self._stats[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._stats.get(key, default)

    def get_stats(self) -> dict[str, Any]:
        return dict(self._stats)

    def __repr__(self) -> str:
        return "StatsCollector(%r)" % self._stats
