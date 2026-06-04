"""Tests for the data extractors."""

from crawley.extractors import (
    CSSExtractor,
    PyQueryExtractor,
    RawExtractor,
    XPathExtractor,
)

HTML = '<html><body><h1>Hi</h1><a class="lnk" href="/x">link</a></body></html>'


def test_xpath_extractor():
    tree = XPathExtractor().get_object(HTML)
    assert tree.xpath("//h1")[0].text == "Hi"


def test_pyquery_extractor():
    pq = PyQueryExtractor().get_object(HTML)
    assert pq("h1").text() == "Hi"
    assert pq("a.lnk").attr("href") == "/x"


def test_css_extractor():
    tree = CSSExtractor().get_object(HTML)
    nodes = tree.getroot().cssselect("a.lnk")
    assert nodes and nodes[0].get("href") == "/x"


def test_raw_extractor():
    assert RawExtractor().get_object(HTML) == HTML
