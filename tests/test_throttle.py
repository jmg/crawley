"""Tests for the per-host rate limiter."""

import asyncio
import time

from crawley.http.throttle import HostRateLimiter


async def test_throttle_spaces_requests():
    limiter = HostRateLimiter(delay=0.05)
    start = time.monotonic()
    await limiter.throttle("host")
    await limiter.throttle("host")
    await limiter.throttle("host")
    elapsed = time.monotonic() - start
    # Three calls -> at least two spacing gaps of 0.05s.
    assert elapsed >= 0.09


async def test_no_delay_is_noop():
    limiter = HostRateLimiter(delay=0)
    start = time.monotonic()
    for _ in range(5):
        await limiter.throttle("host")
    assert time.monotonic() - start < 0.05


async def test_different_hosts_not_blocked():
    limiter = HostRateLimiter(delay=0.2)
    start = time.monotonic()
    await asyncio.gather(limiter.throttle("a"), limiter.throttle("b"))
    # Different hosts don't wait on each other.
    assert time.monotonic() - start < 0.1


# async so a running event loop exists: asyncio.Semaphore() raises "no current
# event loop" if constructed outside one on Python <=3.11 (pytest-asyncio 0.23+
# no longer provides a loop for sync tests). In production semaphore() is only
# ever called from async request paths, so a loop is always present there.
async def test_semaphore_only_when_capped():
    assert HostRateLimiter().semaphore("h") is None

    limiter = HostRateLimiter(max_per_host=2)
    sem = limiter.semaphore("h")
    assert isinstance(sem, asyncio.Semaphore)
    # Same host returns the same semaphore instance.
    assert limiter.semaphore("h") is sem


async def test_set_delay_overrides_per_host():
    limiter = HostRateLimiter(delay=0)
    limiter.set_delay("slow", 0.05)
    start = time.monotonic()
    await limiter.throttle("slow")
    await limiter.throttle("slow")
    assert time.monotonic() - start >= 0.04
