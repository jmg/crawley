"""Adaptive per-host throttling.

Adjusts the delay applied to each host based on the observed response latency,
aiming to keep roughly ``target_concurrency`` requests in flight per host (the
same idea as Scrapy's AutoThrottle).
"""

from __future__ import annotations

from typing import Optional


class AutoThrottle:
    """Compute a per-host delay from observed latencies."""

    def __init__(
        self,
        target_concurrency: float = 1.0,
        start_delay: float = 1.0,
        max_delay: float = 60.0,
        enabled: bool = True,
    ) -> None:
        self.target_concurrency = max(target_concurrency, 0.01)
        self.start_delay = start_delay
        self.max_delay = max_delay
        self.enabled = enabled
        self._delays: dict[str, float] = {}

    def adjust(self, host: str, latency: Optional[float]) -> float:
        """Update and return the new delay for *host* given a *latency*."""
        previous = self._delays.get(host, self.start_delay)
        if latency is None:
            return previous

        target = latency / self.target_concurrency
        # Smooth towards the target and clamp to [0, max_delay].
        new_delay = (previous + target) / 2
        new_delay = min(max(new_delay, 0.0), self.max_delay)
        self._delays[host] = new_delay
        return new_delay
