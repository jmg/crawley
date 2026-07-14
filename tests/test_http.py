"""Tests for the async HTTP layer."""

import os

import pytest

from crawley.extractors import XPathExtractor
from crawley.http.cookies import CookieHandler
from crawley.http.managers import FastRequestManager, RequestManager


async def test_make_request_get(server):
    manager = FastRequestManager()
    try:
        response = await manager.make_request(
            server + "/page1", extractor=XPathExtractor()
        )
        assert response.status_code == 200
        assert "Title 1" in response.raw_html
        assert response.html.xpath("//h1")[0].text == "Title 1"
    finally:
        await manager.aclose()


async def test_make_request_post(server):
    manager = FastRequestManager()
    try:
        response = await manager.make_request(server + "/echo", data={"k": "v"})
        assert "posted" in response.raw_html
        assert "k=v" in response.raw_html
    finally:
        await manager.aclose()


async def test_retries_then_raises():
    from crawley.http.retry import RetryPolicy

    manager = RequestManager(delay=0, deviation=0)
    manager.retry_policy = RetryPolicy(max_retries=1, backoff_factor=0)
    with pytest.raises(Exception):
        await manager.make_request("http://127.0.0.1:1/never")
    await manager.aclose()


async def test_get_body_is_size_capped_not_discarded(server, monkeypatch):
    # An oversized body must be TRUNCATED to the cap, never discarded to "" — a
    # discarded body would cache an empty 200 and silently lose the page.
    from crawley import config

    monkeypatch.setattr(config, "MAX_RESPONSE_BYTES", 50)
    manager = RequestManager(delay=0, deviation=0)
    try:
        response = await manager.make_request(server + "/page1")
        assert response.status_code == 200
        assert 0 < len(response.raw_html) <= 50
    finally:
        await manager.aclose()


async def test_post_body_is_size_capped(server, monkeypatch):
    from crawley import config

    monkeypatch.setattr(config, "MAX_RESPONSE_BYTES", 50)
    manager = RequestManager(delay=0, deviation=0)
    try:
        response = await manager.make_request(server + "/echo", data={"k": "v"})
        assert 0 < len(response.raw_html) <= 50
    finally:
        await manager.aclose()


async def test_ssrf_hook_blocks_loopback_when_enabled(server):
    from crawley.http.retry import RetryPolicy

    class _S:
        SSRF_PROTECT = True

    manager = RequestManager(
        settings=_S(), delay=0, deviation=0, retry_policy=RetryPolicy(max_retries=0)
    )
    try:
        # The default guard blocks 127.0.0.1 (loopback) on every request.
        with pytest.raises(Exception):
            await manager.make_request(server + "/page1")
    finally:
        await manager.aclose()


async def test_ssrf_hook_off_by_default(server):
    # Without SSRF_PROTECT the loopback test server is reachable (dev default).
    manager = RequestManager(delay=0, deviation=0)
    try:
        response = await manager.make_request(server + "/page1")
        assert response.status_code == 200
    finally:
        await manager.aclose()


def test_cookie_handler_roundtrip(tmp_path):
    cookie_file = os.path.join(tmp_path, "cookies")
    handler = CookieHandler(cookie_file=cookie_file)
    assert isinstance(handler.cookie_file, str)
    # Saving an empty jar should create the file and loading it back must work.
    handler.save_cookies()
    handler.load_cookies()
