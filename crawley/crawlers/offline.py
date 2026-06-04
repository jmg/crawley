"""A crawler that rewrites relative asset urls to absolute ones.

Useful to save pages for offline viewing: ``<link href>`` and ``<img src>``
attributes are rewritten so the page renders without the original server.
"""

from lxml import etree

from crawley.crawlers.base import BaseCrawler
from crawley.extractors import XPathExtractor
from crawley.http.urls import UrlFinder


class OffLineCrawler(BaseCrawler):
    """A crawler that fixes relative asset urls in the fetched html."""

    async def _get_response(self, url, data=None):
        response = await super()._get_response(url, data)

        fixer = HTMLFixer(UrlFinder._url_regex, url, response.raw_html)
        response.raw_html = fixer.get_fixed_html()
        response.html = self.extractor.get_object(response.raw_html)

        return response


class HTMLFixer:
    """Rewrite relative ``link``/``img`` urls into absolute ones."""

    def __init__(self, url_regex, url, html):
        self._url_regex = url_regex
        self.url = url
        self.html_tree = XPathExtractor().get_object(html)

    def get_fixed_html(self):
        self._fix_tags("link", "href")
        self._fix_tags("img", "src")
        return etree.tostring(
            self.html_tree.getroot(), pretty_print=True, method="html"
        ).decode("utf-8")

    def _fix_tags(self, tag, attrib):
        for node in self.html_tree.xpath("//%s" % tag):
            value = node.attrib.get(attrib)
            if value and not self._url_regex.match(value):
                node.attrib[attrib] = "%s/%s" % (self.url.rstrip("/"), value.lstrip("/"))
