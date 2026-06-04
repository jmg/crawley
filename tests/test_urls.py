"""Tests for the UrlFinder."""

from crawley.http.response import Response
from crawley.http.urls import UrlFinder

HTML = """
<html><body>
  <a href="/abs">absolute path</a>
  <a href="rel">relative</a>
  <a href="https://other.com/x">external</a>
  <a href="//proto.com/y">protocol relative</a>
</body></html>
"""


def _response(url="http://site.com/dir/page"):
    return Response(raw_html=HTML, url=url)


def test_regular_urls_are_resolved():
    urls = UrlFinder(_response()).get_urls()
    assert "http://site.com/abs" in urls
    assert "http://site.com/dir/rel" in urls
    assert "https://other.com/x" in urls
    assert "http://proto.com/y" in urls


def test_hidden_urls():
    html = HTML + "plain text http://hidden.com/path more"
    response = Response(raw_html=html, url="http://site.com/")
    urls = UrlFinder(response, search_hidden_urls=True).get_urls()
    assert any("hidden.com" in u for u in urls)
