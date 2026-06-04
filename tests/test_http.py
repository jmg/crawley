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
    manager = RequestManager(delay=0, deviation=0)
    manager.MAX_TRIES = 1
    with pytest.raises(Exception):
        await manager.make_request("http://127.0.0.1:1/never")
    await manager.aclose()


def test_cookie_handler_roundtrip(tmp_path):
    cookie_file = os.path.join(tmp_path, "cookies")
    handler = CookieHandler(cookie_file=cookie_file)
    assert isinstance(handler.cookie_file, str)
    # Saving an empty jar should create the file and loading it back must work.
    handler.save_cookies()
    handler.load_cookies()
