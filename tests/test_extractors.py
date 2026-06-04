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


MULTI = """
<html><body>
  <ul><li>a</li><li>b</li><li>c</li></ul>
  <a href="/1">one</a><a href="/2">two</a>
</body></html>
"""


def test_xpath_multiple_nodes():
    tree = XPathExtractor().get_object(MULTI)
    items = [li.text for li in tree.xpath("//li")]
    assert items == ["a", "b", "c"]


def test_pyquery_iteration():
    pq = PyQueryExtractor().get_object(MULTI)
    hrefs = [a.get("href") for a in pq("a")]
    assert hrefs == ["/1", "/2"]


def test_css_multiple_nodes():
    tree = CSSExtractor().get_object(MULTI)
    items = [li.text for li in tree.getroot().cssselect("ul li")]
    assert items == ["a", "b", "c"]


def test_extractors_share_base():
    from crawley.extractors import BaseExtractor

    for cls in (XPathExtractor, PyQueryExtractor, CSSExtractor, RawExtractor):
        assert issubclass(cls, BaseExtractor)
