"""Tests for the url matchers (ported from the legacy suite)."""

from crawley.utils import matcher, url_matcher


def test_url_matcher_true():
    assert url_matcher("http://www.google.com.ar", "%www.google.com%")
    assert url_matcher("http://www.google.com.ar", "http://www.google.com%")
    assert url_matcher("http://www.google.com.ar", "%www.google.com.ar")
    assert url_matcher("http://www.google.com.ar", "http://www.google.com.ar")


def test_url_matcher_false():
    assert not url_matcher("http://www.google.com.ar", "%www.google.com")
    assert not url_matcher("http://www.google.com.ar", "www.google.com%")
    assert not url_matcher("http://www.google.com.ar", "%www.goo.com%")
    assert not url_matcher("http://www.google.com.ar", "http://www.goo.com.ar")


def test_strict_matcher():
    assert matcher("http://www.a.com", "http://www.a.com")
    assert matcher("www.a.com", "http://www.a.com", False)
    assert not matcher("patron_fruta", "http://www.a.com")
