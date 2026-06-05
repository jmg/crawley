"""Tests for the DSL INI config parser and the CrawlerCompiler."""

import pytest

from crawley.simple_parser.config_parser import ConfigApp, ConfigObj


def test_config_obj_set_get():
    config = ConfigObj()
    config[("crawler", "start_urls")] = "http://a,http://b"
    assert config[("crawler", "start_urls")] == "http://a,http://b"
    assert config[("crawler", "missing")] is None


def test_config_obj_none_becomes_empty():
    config = ConfigObj()
    config[("s", "k")] = None
    assert config[("s", "k")] == ""


def test_config_obj_save_and_app_read(tmp_path):
    config = ConfigObj()
    config[("crawler", "max_depth")] = "3"
    target = tmp_path / "config.ini"
    config.save(str(target))

    app = ConfigApp(str(tmp_path))
    assert app[("crawler", "max_depth")] == "3"


def test_crawler_compiler():
    pytest.importorskip("sqlalchemy")
    from crawley.simple_parser.compilers import CrawlerCompiler

    config = ConfigObj()
    config[("crawler", "start_urls")] = "http://a.test,http://b.test"
    config[("crawler", "max_depth")] = "2"

    crawler_class = CrawlerCompiler(scrapers=["fake"], config=config).compile()
    assert crawler_class.start_urls == ["http://a.test", "http://b.test"]
    assert crawler_class.max_depth == 2
    assert crawler_class.scrapers == ["fake"]
