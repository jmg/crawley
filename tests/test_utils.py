"""Tests for the utility helpers."""

import os
import types

import pytest

from crawley.utils import (
    add_to_path,
    check_for_file,
    fix_file_extension,
    get_settings_attribute,
    has_valid_attr,
    search_class,
)
from crawley.utils.matchers import complex_matcher

# -- matchers ---------------------------------------------------------------


def test_complex_matcher_match():
    assert complex_matcher(r"[a-z]+", "abc") is True
    assert complex_matcher(r"\d+", "abc123", strict=False) is True


def test_complex_matcher_no_match():
    assert complex_matcher("xyz", "abc") is False


# -- files ------------------------------------------------------------------


def test_fix_file_extension():
    assert fix_file_extension("db", "sqlite") == "db.sqlite"
    assert fix_file_extension("db.sqlite", "sqlite") == "db.sqlite"


def test_has_valid_attr():
    settings = types.SimpleNamespace(A="x", B="", C=None)
    assert has_valid_attr(settings, "A")
    assert not has_valid_attr(settings, "B")
    assert not has_valid_attr(settings, "C")
    assert not has_valid_attr(settings, "MISSING")


def test_get_settings_attribute():
    settings = types.SimpleNamespace(A="x", B="")
    assert get_settings_attribute(settings, "A") == "x"
    assert get_settings_attribute(settings, "B", default="d") == "d"
    assert get_settings_attribute(settings, "MISSING", default="d") == "d"


def test_check_for_file(tmp_path):
    settings = types.SimpleNamespace(PROJECT_ROOT=str(tmp_path))
    assert not check_for_file(settings, "x.txt")
    (tmp_path / "x.txt").write_text("hi")
    assert check_for_file(settings, "x.txt")


# -- common -----------------------------------------------------------------


def test_search_class():
    class Base:
        pass

    class Child(Base):
        pass

    assert search_class(Base, [Base, Child]) is Child
    assert search_class(Base, [Base]) is None


def test_add_to_path():
    marker = "/tmp/crawley-test-path-xyz"
    add_to_path(marker)
    import sys

    assert sys.path[0] == marker
    sys.path.remove(marker)


def test_exit_with_error():
    from crawley.utils import exit_with_error

    with pytest.raises(SystemExit):
        exit_with_error("boom")


# -- projects ---------------------------------------------------------------


def test_get_full_template_path():
    from crawley.utils import get_full_template_path

    path = get_full_template_path("settings")
    assert path.endswith(os.path.join("templates", "settings.tm"))


def test_import_user_module_missing_exits():
    from crawley.utils import import_user_module

    with pytest.raises(SystemExit):
        import_user_module("definitely_not_a_real_module_xyz")


def test_import_user_module_missing_no_exit():
    from crawley.utils import import_user_module

    assert import_user_module("definitely_not_a_real_module_xyz", exit=False) is None
