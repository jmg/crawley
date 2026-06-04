"""Tests for the retry policy and its integration."""

import uuid
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx

from crawley.http.managers import FastRequestManager
from crawley.http.retry import RetryPolicy


class _Resp:
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers or {}


def test_should_retry_on_status():
    policy = RetryPolicy(max_retries=3)
    assert policy.should_retry(0, response=_Resp(503))
    assert policy.should_retry(0, response=_Resp(429))
    assert not policy.should_retry(0, response=_Resp(200))


def test_should_retry_respects_max():
    policy = RetryPolicy(max_retries=2)
    assert policy.should_retry(1, response=_Resp(503))
    assert not policy.should_retry(2, response=_Resp(503))


def test_should_retry_on_transport_error():
    policy = RetryPolicy(max_retries=3)
    assert policy.should_retry(0, exception=httpx.ConnectError("boom"))
    assert not policy.should_retry(0, exception=ValueError("nope"))


def test_backoff_is_exponential_and_capped():
    policy = RetryPolicy(backoff_factor=1, max_backoff=10, jitter=False)
    assert policy.backoff_time(0) == 1
    assert policy.backoff_time(1) == 2
    assert policy.backoff_time(2) == 4
    assert policy.backoff_time(10) == 10  # capped


def test_backoff_jitter_in_range():
    policy = RetryPolicy(backoff_factor=1, jitter=True)
    for _ in range(20):
        value = policy.backoff_time(2)  # base 4
        assert 2.0 <= value <= 4.0


def test_retry_after_seconds():
    policy = RetryPolicy()
    assert policy.backoff_time(5, response=_Resp(503, {"Retry-After": "7"})) == 7.0


def test_retry_after_http_date():
    policy = RetryPolicy()
    when = datetime.now(timezone.utc) + timedelta(seconds=30)
    header = format_datetime(when, usegmt=True)
    value = policy.backoff_time(0, response=_Resp(503, {"Retry-After": header}))
    assert 20 <= value <= 31


async def test_manager_retries_until_success(server):
    key = uuid.uuid4().hex
    manager = FastRequestManager(
        retry_policy=RetryPolicy(max_retries=3, backoff_factor=0)
    )
    try:
        resp = await manager.make_request(
            server + "/flaky?fail=2&key=" + key
        )
        assert resp.status_code == 200
        assert "Title ok" in resp.raw_html
    finally:
        await manager.aclose()


async def test_manager_gives_up_returns_last_response(server):
    manager = FastRequestManager(
        retry_policy=RetryPolicy(max_retries=1, backoff_factor=0)
    )
    try:
        resp = await manager.make_request(server + "/always-503")
        assert resp.status_code == 503
    finally:
        await manager.aclose()
