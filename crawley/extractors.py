"""Data extractor classes.

An extractor turns the raw html of a page into a convenient object so the
user can scrape it with their favourite tool (XPath, a jQuery-like API or
CSS selectors).
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from lxml import etree
from pyquery import PyQuery


class BaseExtractor:
    """Interface for every extractor."""

    def get_object(self, data: str) -> Any:  # pragma: no cover - interface only
        raise NotImplementedError


class PyQueryExtractor(BaseExtractor):
    """Extractor using PyQuery (a jQuery-like library for Python)."""

    def get_object(self, data: str) -> PyQuery:
        return PyQuery(data)


class XPathExtractor(BaseExtractor):
    """Extractor exposing an :mod:`lxml` tree, ready to be queried via XPath."""

    def get_object(self, data: str) -> Any:
        parser = etree.HTMLParser()
        # Parse from bytes so documents carrying an XML encoding declaration
        # (e.g. sitemaps) don't raise "Unicode strings with encoding declaration".
        return etree.parse(BytesIO(data.encode("utf-8")), parser)


class CSSExtractor(BaseExtractor):
    """Extractor exposing an :mod:`lxml` tree queryable with CSS selectors.

    The returned tree supports ``tree.cssselect("div.foo a")`` thanks to the
    ``cssselect`` package.
    """

    def get_object(self, data: str) -> Any:
        parser = etree.HTMLParser()
        # Parse from bytes so documents carrying an XML encoding declaration
        # (e.g. sitemaps) don't raise "Unicode strings with encoding declaration".
        return etree.parse(BytesIO(data.encode("utf-8")), parser)


class RawExtractor(BaseExtractor):
    """Returns the raw html data untouched."""

    def get_object(self, data: str) -> str:
        return data
