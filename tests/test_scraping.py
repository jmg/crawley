"""Tests for the high level scraping API (crawley.scraping)."""

import pytest

from crawley.scraping import (
    Document,
    Element,
    _split_pseudo,
    afetch,
    afetch_all,
    fetch,
    parse,
    scrape,
)

HTML = """
<html><head><title>Quotes</title></head><body>
  <h1 id="main">All quotes</h1>
  <div class="quote">
    <span class="text">The quote one</span>
    <small class="author">Author One</small>
    <a class="tag" href="/tag/a">a</a>
    <a class="tag" href="/tag/b">b</a>
  </div>
  <div class="quote">
    <span class="text">The quote two</span>
    <small class="author">Author Two</small>
  </div>
  <a class="next" href="page2">Next</a>
  <img src="img/logo.png">
</body></html>
"""


@pytest.fixture
def doc():
    return parse(HTML, url="http://books.test/list/")


# -- pseudo selector parsing ------------------------------------------------


def test_split_pseudo_plain():
    assert _split_pseudo("div.foo") == ("div.foo", None, None)


def test_split_pseudo_text():
    assert _split_pseudo("span.text::text") == ("span.text", "text", None)


def test_split_pseudo_attr():
    assert _split_pseudo("a::attr(href)") == ("a", "attr", "href")


# -- Document / Element -----------------------------------------------------


def test_title(doc):
    assert doc.title == "Quotes"


def test_css_returns_elements(doc):
    quotes = doc.css("div.quote")
    assert len(quotes) == 2
    assert all(isinstance(q, Element) for q in quotes)


def test_css_first(doc):
    assert doc.css_first("h1").text == "All quotes"
    assert doc.css_first("h1").attr("id") == "main"
    assert doc.css_first(".missing") is None


def test_css_text_pseudo(doc):
    assert doc.css("span.text::text") == ["The quote one", "The quote two"]


def test_css_attr_pseudo(doc):
    hrefs = doc.css("a.tag::attr(href)")
    assert hrefs == ["http://books.test/tag/a", "http://books.test/tag/b"]


def test_element_attrs_and_html(doc):
    h1 = doc.css_first("h1")
    assert h1.attrs == {"id": "main"}
    assert h1.tag == "h1"
    assert "<h1" in h1.html


def test_nested_element_query(doc):
    first = doc.css_first("div.quote")
    assert first.css_first("span.text").text == "The quote one"
    assert first.css("a.tag::text") == ["a", "b"]


def test_xpath(doc):
    assert doc.xpath("//h1/text()") == ["All quotes"]
    nodes = doc.xpath("//small")
    assert nodes[0].text == "Author One"


def test_links_absolute(doc):
    links = doc.links()
    assert "http://books.test/tag/a" in links
    assert "http://books.test/list/page2" in links
    # de-duplicated
    assert len(links) == len(set(links))


def test_extract_single_and_list(doc):
    data = doc.extract(
        {
            "title": "h1::text",
            "first_author": "small.author::text",
            "all_authors": ["small.author::text"],
            "logo": "img::attr(src)",
        }
    )
    assert data["title"] == "All quotes"
    assert data["first_author"] == "Author One"
    assert data["all_authors"] == ["Author One", "Author Two"]
    assert data["logo"] == "http://books.test/list/img/logo.png"


def test_extract_default_text_without_pseudo(doc):
    data = doc.extract({"authors": ["small.author"]})
    assert data["authors"] == ["Author One", "Author Two"]


def test_extract_missing_returns_none(doc):
    assert doc.extract({"x": ".nope"})["x"] is None


def test_parse_empty_html():
    d = parse("", url="http://x.test/")
    assert isinstance(d, Document)
    assert d.css("div") == []


# -- network helpers (against the local server) -----------------------------


def test_fetch(server):
    doc = fetch(server + "/page1")
    assert doc.css_first("h1").text == "Title 1"
    assert doc.url.endswith("/page1")


def test_scrape(server):
    data = scrape(server + "/page1", {"title": "h1::text", "author": "p.author::text"})
    assert data == {"title": "Title 1", "author": "Author 1"}


async def test_afetch(server):
    doc = await afetch(server + "/page2")
    assert doc.css_first("h1").text == "Title 2"


async def test_afetch_all(server):
    docs = await afetch_all([server + "/page1", server + "/page2", server + "/missing-x"])
    assert docs[0].css_first("h1").text == "Title 1"
    assert docs[1].css_first("h1").text == "Title 2"
    # 404 still returns a parseable document (not an exception here)
    assert docs[2] is not None


async def test_afetch_all_handles_errors():
    docs = await afetch_all(["http://127.0.0.1:1/down"])
    assert docs == [None]


async def test_afetch_with_shared_client(server):
    import httpx

    async with httpx.AsyncClient() as client:
        doc = await afetch(server + "/page1", client=client)
    assert doc.css_first("h1").text == "Title 1"


def test_element_text_attr_defaults():
    doc = parse("<html><body><p>hi</p></body></html>")
    p = doc.css_first("p")
    assert p.attr("missing", "fallback") == "fallback"
    assert p.attrs == {}


def test_repr_smoke():
    doc = parse("<html><body><h1>x</h1></body></html>", url="http://x/")
    assert "Document" in repr(doc)
    assert "Element" in repr(doc.css_first("h1"))
