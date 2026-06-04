"""Retry policy with exponential backoff and jitter.

Decides whether a failed request (a network error or a retryable HTTP status
such as 429/503) should be retried and for how long to wait before doing so,
honouring the ``Retry-After`` response header when present.
"""

import asyncio
import datetime
import random
from email.utils import parsedate_to_datetime

import httpx

from crawley import config


class RetryPolicy:
    """Configurable retry/backoff strategy."""

    def __init__(
        self,
        max_retries=None,
        backoff_factor=None,
        max_backoff=None,
        statuses=None,
        jitter=True,
    ):
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

    def should_retry(self, attempt, response=None, exception=None):
        """Return ``True`` if a further attempt should be made."""
        if attempt >= self.max_retries:
            return False
        if exception is not None:
            return isinstance(exception, httpx.TransportError)
        if response is not None:
            return response.status_code in self.statuses
        return False

    def backoff_time(self, attempt, response=None):
        """Seconds to wait before retry number *attempt* (0-based)."""
        if response is not None:
            retry_after = self._retry_after(response)
            if retry_after is not None:
                return retry_after

        backoff = self.backoff_factor * (2**attempt)
        backoff = min(backoff, self.max_backoff)
        if self.jitter and backoff > 0:
            # Full jitter in the [backoff/2, backoff] range.
            backoff = backoff * (0.5 + random.random() / 2)
        return backoff

    async def sleep(self, seconds):
        if seconds > 0:
            await asyncio.sleep(seconds)

    @staticmethod
    def _retry_after(response):
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
        now = datetime.datetime.now(when.tzinfo)
        return max(0.0, (when - now).total_seconds())
