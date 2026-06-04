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
