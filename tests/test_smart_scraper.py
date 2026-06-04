"""Tests for the SmartScraper (html structure similarity)."""

from crawley.extractors import XPathExtractor
from crawley.http.response import Response
from crawley.scrapers.smart import HtmlSchema, SmartScraper


def _response(url, html):
    return Response(
        raw_html=html,
        extracted_html=XPathExtractor().get_object(html),
        url=url,
    )


def test_html_schema():
    schema = HtmlSchema()
    schema.feed("<html><body><h1>x</h1><p>y</p></body></html>")
    assert schema.get_schema() == "html/body/h1/p"


def test_requires_template_url():
    import pytest

    class S(SmartScraper):
        matching_urls = ["%"]

    with pytest.raises(ValueError):
        S()


SIMILAR = "<html><body><h1>Other title</h1><p>other</p><div>z</div></body></html>"
DIFFERENT = "<html><body><a>1</a><a>2</a><a>3</a><a>4</a><a>5</a></body></html>"


def test_smart_scraper_matches_similar_structure(server):
    collected = []

    class S(SmartScraper):
        matching_urls = ["%/page%"]
        template_url = server + "/page1"

        def scrape(self, response):
            collected.append(response.html.xpath("//h1")[0].text)

    scraper = S()

    # A page with the same structure as the template gets scraped...
    scraper.try_scrape(_response(server + "/page9", SIMILAR))
    assert collected == ["Other title"]

    # ...a structurally different page does not.
    collected.clear()
    scraper.try_scrape(_response(server + "/page9", DIFFERENT))
    assert collected == []
