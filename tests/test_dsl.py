"""Tests for the DSL parser / compiler."""

import pytest

from crawley.exceptions import TemplateSyntaxError
from crawley.simple_parser import Generator
from crawley.simple_parser.parsers import DSLAnalizer


def test_parse_blocks():
    dsl = """PAGE => http://example.com/
             table1.col1 -> /html/body/h1
             table1.col2 -> /html/body/p"""
    blocks = DSLAnalizer(dsl).parse()
    assert len(blocks) == 1
    header = blocks[0][0]
    assert header.is_header
    assert header.xpath == "http://example.com/"
    assert blocks[0][1].field == {"table": "table1", "column": "col1"}


def test_syntax_errors():
    pytest.importorskip("sqlalchemy")
    with pytest.raises(TemplateSyntaxError):
        Generator("my_model -> /html -> other", settings=None)
    with pytest.raises(TemplateSyntaxError):
        Generator("my_model = /html/body", settings=None)


def test_generate_entities_and_scrapers(server):
    pytest.importorskip("sqlalchemy")
    dsl = (
        "PAGE => %s/page1\n" % server
        + "dslpkg.title -> /html/body/h1\n"
        + "dslpkg.author -> /html/body/p"
    )
    generator = Generator(dsl, settings=None)

    entities = generator.gen_entities()
    assert any(e.__name__ == "dslpkg" for e in entities)

    scrapers = generator.gen_scrapers()
    assert len(scrapers) == 1
    assert scrapers[0].template_url == server + "/page1"


def test_parse_multiple_blocks():
    dsl = (
        "PAGE => http://a.test/\n"
        "t1.c1 -> /html/h1\n"
        "PAGE => http://b.test/\n"
        "t2.c1 -> /html/h2\n"
    )
    blocks = DSLAnalizer(dsl).parse()
    assert len(blocks) == 2
    assert blocks[0][0].xpath == "http://a.test/"
    assert blocks[1][0].xpath == "http://b.test/"


def test_generated_scraper_scrapes(server):
    pytest.importorskip("sqlalchemy")
    from crawley.extractors import XPathExtractor
    from crawley.http.response import Response
    from crawley.persistance.relational.databases import session, setup

    dsl = (
        "PAGE => %s/page1\n" % server
        + "dslscrape.title -> /html/body/h1\n"
    )
    generator = Generator(dsl, settings=None)
    generator.gen_entities()
    setup("sqlite:///:memory:")
    scraper_class = generator.gen_scrapers()[0]

    scraper = scraper_class()
    html = "<html><body><h1>Title 1</h1><p>x</p><div>y</div></body></html>"
    response = Response(
        raw_html=html, extracted_html=XPathExtractor().get_object(html),
        url=server + "/page1",
    )
    scraper.scrape(response)

    rows = session.query(generator.interpreter.entities["dslscrape"]).all()
    assert rows and rows[0].title == "Title 1"
    session.remove()
