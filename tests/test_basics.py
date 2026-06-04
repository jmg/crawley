"""Tests for config, exceptions and the toolbox."""

import pytest

import crawley
from crawley import config
from crawley.exceptions import (
    AuthenticationError,
    CrawleyError,
    ScraperCantParseError,
    TemplateSyntaxError,
)


def test_version_exposed():
    assert isinstance(crawley.__version__, str)
    assert crawley.__version__.count(".") >= 1


def test_public_api_is_lazily_importable():
    for name in crawley.__all__:
        assert getattr(crawley, name) is not None


def test_unknown_attribute_raises():
    with pytest.raises(AttributeError):
        crawley.does_not_exist


def test_config_defaults():
    assert config.MAX_CONCURRENCY > 0
    assert config.REQUEST_DELAY >= 0
    assert "Mozilla" in config.MOZILLA_USER_AGENT


def test_exception_hierarchy():
    for exc in (AuthenticationError, ScraperCantParseError, TemplateSyntaxError):
        assert issubclass(exc, CrawleyError)


def test_template_syntax_error_keeps_line():
    err = TemplateSyntaxError(7, "boom")
    assert err.line == 7


def test_toolbox_request(server):
    from crawley.toolbox import request

    resp = request(server + "/page1")
    assert resp.status_code == 200
    assert resp.css_first("h1").text == "Title 1"
