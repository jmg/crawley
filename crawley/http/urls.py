"""Discover urls inside html pages."""

from re import compile as re_compile
from urllib.parse import urljoin, urlparse

from crawley.extractors import XPathExtractor


class UrlFinder:
    """Find urls in html documents."""

    _url_regex = re_compile(
        r"(https?://)([a-zA-Z0-9]+\.[a-zA-Z0-9\-]+|[a-zA-Z0-9\-]+)"
        r"\.[a-zA-Z\.]{2,6}(/[a-zA-Z0-9\.\?=/#%&\+-]+|/|)"
    )

    def __init__(self, response, search_hidden_urls=False):
        self.response = response
        self.search_hidden_urls = search_hidden_urls

    def get_urls(self):
        """Return a set of urls found in the current html page."""
        urls = self.search_regulars()

        if self.search_hidden_urls:
            urls = self.search_hiddens(urls)

        return urls

    def search_regulars(self):
        """Search urls inside the ``<a>`` tags."""
        urls = set()

        tree = XPathExtractor().get_object(self.response.raw_html)

        for link_tag in tree.xpath("//a"):
            href = link_tag.attrib.get("href")
            if not href:
                continue

            url = self._normalize_url(href)
            if url:
                urls.add(url)

        return urls

    def _normalize_url(self, url):
        """Resolve relative urls against the response url."""
        url = url.strip()

        if url.startswith("//"):
            scheme = urlparse(self.response.url).scheme or "http"
            return "%s:%s" % (scheme, url)

        if not urlparse(url).netloc:
            return urljoin(self.response.url, url)

        return url

    def search_hiddens(self, urls):
        """Search the entire html for urls via a regex."""
        for url_match in self._url_regex.finditer(self.response.raw_html):
            urls.add(url_match.group(0))
        return urls
