"""Shared pytest fixtures.

The crawler is exercised against a real, local, throw-away HTTP server so the
tests are hermetic and never touch the network.
"""

import http.server
import socketserver
import threading
from urllib.parse import parse_qs, urlparse

import pytest

# Per-key hit counters used by the "/flaky" endpoint (shared, thread-safe).
_FLAKY_COUNTERS = {}
_FLAKY_LOCK = threading.Lock()

ROBOTS = "User-agent: *\nDisallow: /private\n"

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

    def _send_status(self, status, body="", retry_after=None):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        if retry_after is not None:
            self.send_header("Retry-After", str(retry_after))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/robots.txt":
            self._send(ROBOTS)
        elif path == "/flaky":
            self._handle_flaky()
        elif path == "/always-503":
            self._send_status(503, "<html><body>down</body></html>", retry_after=0)
        elif path == "/" or path == "":
            self._send(INDEX)
        elif path.startswith("/private"):
            self._send(PAGE.format(n="private"))
        elif path.startswith("/page"):
            n = path.rstrip("/").split("page")[-1] or "x"
            self._send(PAGE.format(n=n))
        elif path == "/setcookie":
            self.send_response(200)
            self.send_header("Set-Cookie", "session=abc; Path=/")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>ok</body></html>")
        else:
            self._send("<html><body><h1>404</h1></body></html>", status=404)

    def _handle_flaky(self):
        params = parse_qs(urlparse(self.path).query)
        key = params.get("key", ["default"])[0]
        fail = int(params.get("fail", ["1"])[0])

        with _FLAKY_LOCK:
            count = _FLAKY_COUNTERS.get(key, 0) + 1
            _FLAKY_COUNTERS[key] = count

        if count <= fail:
            self._send_status(503, "<html><body>retry</body></html>", retry_after=0)
        else:
            self._send(PAGE.format(n="ok"))

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


# --------------------------------------------------------------------------
# A second server that mimics the structure of https://quotes.toscrape.com/
# so the documentation examples can run against it (paginated quotes site).
# --------------------------------------------------------------------------

QUOTE = """
  <div class="quote">
    <span class="text">{text}</span>
    <small class="author">{author}</small>
    <div class="tags">{tags}</div>
  </div>"""

QUOTES_PAGES = 3
QUOTES_PER_PAGE = 2


def quotes_page(page):
    quotes = []
    for k in range(1, QUOTES_PER_PAGE + 1):
        tags = "".join(
            '<a class="tag" href="/tag/{t}/">{t}</a>'.format(t=t)
            for t in ("t%d-%d" % (page, k), "common")
        )
        quotes.append(
            QUOTE.format(
                text="Quote %d-%d" % (page, k),
                author="Author %d%d" % (page, k),
                tags=tags,
            )
        )
    next_link = (
        '<li class="next"><a href="/page/%d/">Next</a></li>' % (page + 1)
        if page < QUOTES_PAGES
        else ""
    )
    return (
        "<html><head><title>Quotes</title></head><body>"
        "<h1>Quotes to Scrape</h1>"
        + "".join(quotes)
        + "<ul class='pager'>"
        + next_link
        + "</ul></body></html>"
    )


class _QuotesHandler(http.server.BaseHTTPRequestHandler):
    def _send(self, body, status=200):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/robots.txt":
            self._send("User-agent: *\nAllow: /\n")
        elif path == "/" or path == "":
            self._send(quotes_page(1))
        elif path.startswith("/page/"):
            try:
                page = int(path.strip("/").split("/")[1])
            except (IndexError, ValueError):
                page = 1
            self._send(quotes_page(page))
        elif path.startswith("/tag/"):
            self._send("<html><body><h1>Tag</h1></body></html>")
        else:
            self._send("<html><body><h1>404</h1></body></html>", status=404)

    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def quotes_server():
    """A local server mimicking a paginated quotes site for the examples."""
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _QuotesHandler)
    httpd.daemon_threads = True
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address
    try:
        # Trailing slash so examples can build "<base>page/2/" urls.
        yield "http://%s:%d/" % (host, port)
    finally:
        httpd.shutdown()
        httpd.server_close()
