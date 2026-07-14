"""Retry policy with exponential backoff and jitter.

Decides whether a failed request (a network error or a retryable HTTP status
such as 429/503) should be retried and for how long to wait before doing so,
honouring the ``Retry-After`` response header when present.
"""

import asyncio
import datetime
import random
from email.utils import parsedate_to_datetime
from typing import Any, Iterable, Optional

import httpx

from crawley import config


class RetryPolicy:
    """Configurable retry/backoff strategy."""

    def __init__(
        self,
        max_retries: Optional[int] = None,
        backoff_factor: Optional[float] = None,
        max_backoff: Optional[float] = None,
        statuses: Optional[Iterable[int]] = None,
        jitter: bool = True,
    ) -> None:
        self.max_retries = (
            config.REQUEST_MAX_RETRIES if max_retries is None else max_retries
        )
        self.backoff_factor = (
            config.RETRY_BACKOFF_FACTOR if backoff_factor is None else backoff_factor
        )
        self.max_backoff = (
            config.RETRY_MAX_BACKOFF if max_backoff is None else max_backoff
        )
        self.statuses = frozenset(
            config.RETRY_STATUSES if statuses is None else statuses
        )
        self.jitter = jitter

    def should_retry(
        self,
        attempt: int,
        response: Any = None,
        exception: Optional[BaseException] = None,
    ) -> bool:
        """Return ``True`` if a further attempt should be made."""
        if attempt >= self.max_retries:
            return False
        if exception is not None:
            return isinstance(exception, httpx.TransportError)
        if response is not None:
            return response.status_code in self.statuses
        return False

    def backoff_time(self, attempt: int, response: Any = None) -> float:
        """Seconds to wait before retry number *attempt* (0-based)."""
        if response is not None:
            retry_after = self._retry_after(response)
            if retry_after is not None:
                # Cap Retry-After like the exponential path: a hostile/misconfigured
                # `Retry-After: 86400` would otherwise sleep for a day while holding
                # a concurrency slot, defeating the crawl time backstop.
                return min(retry_after, self.max_backoff)

        # Clamp the exponent before the shift: at attempt >= 1024, 2**attempt is a
        # huge int and coercing it to float (for the min() below) raises
        # OverflowError. 2**30 * backoff_factor already dwarfs max_backoff, so the
        # clamp changes no observable delay.
        backoff = self.backoff_factor * (2 ** min(attempt, 30))
        backoff = min(backoff, self.max_backoff)
        if self.jitter and backoff > 0:
            # Full jitter in the [backoff/2, backoff] range.
            backoff = backoff * (0.5 + random.random() / 2)
        return backoff

    async def sleep(self, seconds: float) -> None:
        if seconds > 0:
            await asyncio.sleep(seconds)

    @staticmethod
    def _retry_after(response: Any) -> Optional[float]:
        """Parse the ``Retry-After`` header (seconds or an HTTP date)."""
        value = response.headers.get("Retry-After")
        if not value:
            return None
        try:
            return max(0.0, float(value))
        except ValueError:
            pass
        try:
            when = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        # An HTTP-date with a "-0000" zone (or asctime form) parses to a NAIVE
        # datetime; treat it as UTC and compare against a UTC `now`, otherwise we
        # subtract a GMT instant from local wall-clock and mis-compute the wait by
        # the worker's UTC offset (stalling, or retrying immediately).
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        return max(0.0, (when - now).total_seconds())
