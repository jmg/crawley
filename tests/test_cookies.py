"""Tests for cookie handling across requests."""

import os

from crawley.http.cookies import CookieHandler
from crawley.http.managers import FastRequestManager


def test_cookie_handler_default_path():
    handler = CookieHandler()
    assert isinstance(handler.cookie_file, str)
    assert "crawley_cookies" in handler.cookie_file


def test_cookie_handler_custom_path(tmp_path):
    path = os.path.join(tmp_path, "jar")
    handler = CookieHandler(cookie_file=path)
    handler.save_cookies()
    assert os.path.exists(path)
    # Reloading the saved (empty) jar must not raise.
    CookieHandler(cookie_file=path).load_cookies()


async def test_cookies_are_captured_from_response(server):
    manager = FastRequestManager()
    try:
        await manager.make_request(server + "/setcookie")
        names = {cookie.name for cookie in manager.cookie_handler.jar}
        assert "session" in names
    finally:
        await manager.aclose()


async def test_cookies_persist_to_disk(server, tmp_path):
    manager = FastRequestManager()
    manager.cookie_handler = CookieHandler(
        cookie_file=os.path.join(tmp_path, "jar")
    )
    # Re-create the client so it binds to the new jar.
    manager._client = None
    try:
        await manager.make_request(server + "/setcookie")
    finally:
        await manager.aclose()
    assert os.path.exists(os.path.join(tmp_path, "jar"))
