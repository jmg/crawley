"""Tests for the Response object and its scraping shortcuts."""

from crawley.http.response import Response

HTML = "<html><body><h1>Hi</h1><a href='/x'>x</a></body></html>"


def test_basic_attributes():
    r = Response(raw_html=HTML, url="http://x.test/")
    assert r.raw_html == HTML
    assert r.url == "http://x.test/"
    assert r.status_code is None
    assert r.headers == {}


def test_doc_shortcut():
    r = Response(raw_html=HTML, url="http://x.test/")
    assert r.css_first("h1").text == "Hi"
    assert r.css("a::attr(href)") == ["http://x.test/x"]
    assert r.extract({"h": "h1::text"}) == {"h": "Hi"}


def test_doc_is_cached():
    r = Response(raw_html=HTML, url="http://x.test/")
    assert r.doc is r.doc


def test_code_alias():
    class _Raw:
        status_code = 200
        headers = {"a": "b"}

    r = Response(raw_html=HTML, url="http://x.test/", response=_Raw())
    assert r.status_code == 200
    assert r.code == 200
    assert r.headers == {"a": "b"}


def test_repr():
    r = Response(raw_html=HTML, url="http://x.test/")
    assert "x.test" in repr(r)
