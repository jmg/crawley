"""Shared pytest fixtures.

The crawler is exercised against a real, local, throw-away HTTP server so the
tests are hermetic and never touch the network.
"""

import http.server
import socketserver
import threading

import pytest

INDEX = """
<html><body>
  <h1>Index</h1>
  <a href="/page1">one</a>
  <a href="/page2">two</a>
  <a href="page3">three</a>
  <a href="https://example.com/external">external</a>
</body></html>
"""

PAGE = """
<html><body>
  <h1>Title {n}</h1>
  <p class="author">Author {n}</p>
  <div id="content">Body {n}</div>
</body></html>
"""

POST_ECHO = "<html><body><h1>posted</h1><p>{body}</p></body></html>"


class _Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body, status=200):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._send(INDEX)
        elif self.path.startswith("/page") or self.path.startswith("/page3"):
            n = self.path.rstrip("/").split("page")[-1] or "x"
            self._send(PAGE.format(n=n))
        elif self.path == "/setcookie":
            self.send_response(200)
            self.send_header("Set-Cookie", "session=abc; Path=/")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>ok</body></html>")
        else:
            self._send("<html><body><h1>404</h1></body></html>", status=404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        self._send(POST_ECHO.format(body=body))

    def log_message(self, *args):  # silence the server
        pass


@pytest.fixture(scope="session")
def server():
    """Start a local HTTP server and yield its base url."""
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _Handler)
    httpd.daemon_threads = True
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    try:
        yield "http://%s:%d" % (host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
