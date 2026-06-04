"""Data extractor classes.

An extractor turns the raw html of a page into a convenient object so the
user can scrape it with their favourite tool (XPath, a jQuery-like API or
CSS selectors).
"""

from io import StringIO

from lxml import etree
from pyquery import PyQuery


class BaseExtractor:
    """Interface for every extractor."""

    def get_object(self, data):  # pragma: no cover - interface only
        raise NotImplementedError


class PyQueryExtractor(BaseExtractor):
    """Extractor using PyQuery (a jQuery-like library for Python)."""

    def get_object(self, data):
        return PyQuery(data)


class XPathExtractor(BaseExtractor):
    """Extractor exposing an :mod:`lxml` tree, ready to be queried via XPath."""

    def get_object(self, data):
        parser = etree.HTMLParser()
        return etree.parse(StringIO(data), parser)


class CSSExtractor(BaseExtractor):
    """Extractor exposing an :mod:`lxml` tree queryable with CSS selectors.

    The returned tree supports ``tree.cssselect("div.foo a")`` thanks to the
    ``cssselect`` package.
    """

    def get_object(self, data):
        parser = etree.HTMLParser()
        return etree.parse(StringIO(data), parser)


class RawExtractor(BaseExtractor):
    """Returns the raw html data untouched."""

    def get_object(self, data):
        return data
