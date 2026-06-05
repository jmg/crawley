"""Tests for the scrapers."""

from crawley.http.response import Response
from crawley.scrapers import BaseScraper


def _response(url, html="<html><body><h1>x</h1></body></html>"):
    from crawley.extractors import XPathExtractor

    return Response(raw_html=html, extracted_html=XPathExtractor().get_object(html), url=url)


def test_try_scrape_matches():
    scraped = []

    class S(BaseScraper):
        matching_urls = ["%/good%"]

        def scrape(self, response):
            scraped.append(response.url)

    s = S()
    s.try_scrape(_response("http://x.com/good/1"))
    assert scraped == ["http://x.com/good/1"]


def test_try_scrape_no_match_returns_none():
    class S(BaseScraper):
        matching_urls = ["%/good%"]

        def scrape(self, response):
            raise AssertionError("should not be called")

    s = S()
    assert s.try_scrape(_response("http://x.com/bad")) is None


def test_scrape_error_is_handled():
    errors = []

    class S(BaseScraper):
        matching_urls = ["%"]

        def scrape(self, response):
            raise ValueError("boom")

        def on_scrape_error(self, response, ex):
            errors.append(str(ex))

    s = S()
    assert s.try_scrape(_response("http://x.com/any")) is None
    assert errors == ["boom"]


def test_get_urls_default_empty():
    class S(BaseScraper):
        matching_urls = ["%"]

        def scrape(self, response):
            pass

    s = S()
    assert s.try_scrape(_response("http://x.com/any")) == []
