"""Tests for AutoThrottle."""

from crawley.http.autothrottle import AutoThrottle
from crawley.http.throttle import HostRateLimiter
from crawley.spider import Spider


def test_adjust_moves_towards_target():
    at = AutoThrottle(target_concurrency=1.0, start_delay=1.0, max_delay=60.0)
    # latency 3s, target concurrency 1 -> target delay 3; smoothed (1+3)/2 = 2
    assert at.adjust("h", 3.0) == 2.0
    # next: previous 2, target 3 -> 2.5
    assert at.adjust("h", 3.0) == 2.5


def test_adjust_respects_concurrency():
    at = AutoThrottle(target_concurrency=2.0, start_delay=2.0)
    # latency 2, target = 2/2 = 1; smoothed (2+1)/2 = 1.5
    assert at.adjust("h", 2.0) == 1.5


def test_adjust_clamps_to_max():
    at = AutoThrottle(start_delay=50.0, max_delay=10.0)
    assert at.adjust("h", 100.0) == 10.0


def test_adjust_none_latency_keeps_previous():
    at = AutoThrottle(start_delay=1.0)
    assert at.adjust("h", None) == 1.0


def test_per_host_independent():
    at = AutoThrottle(start_delay=1.0)
    at.adjust("a", 5.0)
    assert at.adjust("b", 0.0) == 0.5  # b starts from start_delay, not a's


async def test_spider_autothrottle_sets_per_host_delay(server):
    class S(Spider):
        start_urls = [server + "/page1"]
        autothrottle = True
        autothrottle_start_delay = 0.0
        requests_delay = 0

        def parse(self, response):
            pass

    spider = S()
    assert spider._autothrottle is not None
    await spider.start()
    # After one response a per-host delay has been recorded.
    host = server.split("://", 1)[1]
    assert host in spider._autothrottle._delays


def test_autothrottle_uses_rate_limiter_delay_override():
    limiter = HostRateLimiter(delay=0)
    limiter.set_delay("h", 1.23)
    assert limiter._delay_for("h") == 1.23
