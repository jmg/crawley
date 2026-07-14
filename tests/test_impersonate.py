"""Tests for the curl_cffi browser-impersonation client.

Skipped unless the optional ``curl_cffi`` dependency is installed. Exercises the
adapter against a real, local, throw-away HTTP server.
"""

import http.server
import socketserver
import threading

import pytest

from crawley import config
from crawley.http import urlguard
from crawley.http.impersonate import ImpersonateClient, is_available

pytestmark = pytest.mark.skipif(not is_available(), reason="curl_cffi not installed")

_BIG = b"x" * (200 * 1024)  # 200 KB body
_OK = b"<html><body>ok</body></html>"


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence the server
        pass

    def _send(self, body, status=200, headers=None):
        self.send_response(status)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/ok":
            self._send(_OK, headers={"Content-Type": "text/html"})
        elif self.path == "/big":
            self._send(_BIG, headers={"Content-Type": "text/html"})
        elif self.path == "/redir":
            self._send(b"", status=302, headers={"Location": "/ok"})
        else:
            self._send(b"not found", status=404)


@pytest.fixture(scope="module")
def imp_server():
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _Handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    host, port = httpd.server_address
    yield "http://%s:%d" % (host, port)
    httpd.shutdown()
    httpd.server_close()


async def test_basic_get(imp_server):
    c = ImpersonateClient()
    try:
        r = await c.get(imp_server + "/ok")
        assert r.status_code == 200
        assert "ok" in r.text
        assert r.url.endswith("/ok")
    finally:
        await c.aclose()


async def test_body_is_size_capped(imp_server, monkeypatch):
    # A body larger than the cap must be truncated, not buffered whole.
    monkeypatch.setattr(config, "MAX_RESPONSE_BYTES", 1024)
    c = ImpersonateClient()
    try:
        r = await c.get(imp_server + "/big")
        assert r.status_code == 200
        assert 0 < len(r.text) <= 1024  # truncated well below the 200 KB body
    finally:
        await c.aclose()


async def test_follows_redirect(imp_server):
    c = ImpersonateClient()
    try:
        r = await c.get(imp_server + "/redir")
        assert r.status_code == 200
        assert "ok" in r.text
    finally:
        await c.aclose()


async def test_ssrf_gate_blocks_when_enabled(imp_server):
    c = ImpersonateClient(ssrf_protect=True)
    prev = urlguard.current_guard()
    urlguard.set_url_guard(lambda u: False)
    try:
        with pytest.raises(RuntimeError):
            await c.get(imp_server + "/ok")
    finally:
        urlguard.set_url_guard(prev)
        await c.aclose()


async def test_ssrf_off_by_default(imp_server):
    # With ssrf_protect off (the default), even an all-blocking guard is ignored.
    c = ImpersonateClient()
    prev = urlguard.current_guard()
    urlguard.set_url_guard(lambda u: False)
    try:
        r = await c.get(imp_server + "/ok")
        assert r.status_code == 200
    finally:
        urlguard.set_url_guard(prev)
        await c.aclose()
