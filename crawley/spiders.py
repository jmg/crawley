"""Higher-level spiders: rule-based crawling and sitemap crawling.

- :class:`LinkExtractor` extracts (and filters) links from a response.
- :class:`Rule` binds a link extractor to a callback / follow behaviour.
- :class:`CrawlSpider` follows links automatically according to its ``rules``.
- :class:`SitemapSpider` seeds the crawl from one or more ``sitemap.xml`` files.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from lxml import etree

from crawley.spider import Request, Spider


def _as_tuple(value: Any) -> tuple:
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(value)
    return (value,)


class LinkExtractor:
    """Extract links from a response, filtered by allow/deny rules."""

    def __init__(
        self,
        allow: Any = (),
        deny: Any = (),
        restrict_xpaths: Any = (),
        restrict_css: Any = (),
        tags: Any = ("a",),
        attrs: Any = ("href",),
        unique: bool = True,
    ) -> None:
        self.allow = [re.compile(p) for p in _as_tuple(allow)]
        self.deny = [re.compile(p) for p in _as_tuple(deny)]
        self.restrict_xpaths = _as_tuple(restrict_xpaths)
        self.restrict_css = _as_tuple(restrict_css)
        self.tags = _as_tuple(tags)
        self.attrs = _as_tuple(attrs)
        self.unique = unique

    def _allowed(self, href: str) -> bool:
        if any(r.search(href) for r in self.deny):
            return False
        if self.allow and not any(r.search(href) for r in self.allow):
            return False
        return True

    def extract_links(self, response: Any) -> list:
        """Return the (absolute, filtered) links found in *response*."""
        doc = response.doc

        roots: list = []
        for xpath in self.restrict_xpaths:
            roots.extend(
                el for el in doc.xpath(xpath) if hasattr(el, "css")
            )
        for css in self.restrict_css:
            roots.extend(doc.css(css))
        if not roots:
            roots = [doc]

        links: list = []
        for root in roots:
            for tag in self.tags:
                for element in root.css(tag):
                    for attr in self.attrs:
                        href = element.attr(attr)
                        if not href or not self._allowed(href):
                            continue
                        if self.unique and href in links:
                            continue
                        links.append(href)
        return links


class Rule:
    """Bind a :class:`LinkExtractor` to a callback and/or a follow behaviour."""

    def __init__(
        self,
        link_extractor: Optional[LinkExtractor] = None,
        callback: Any = None,
        follow: Optional[bool] = None,
    ) -> None:
        self.link_extractor = link_extractor or LinkExtractor()
        self.callback = callback
        # Like Scrapy: follow defaults to True when there is no callback.
        self.follow = follow if follow is not None else (callback is None)


class CrawlSpider(Spider):
    """A spider that follows links according to a list of :class:`Rule`."""

    rules: list = []

    def parse(self, response: Any) -> Any:
        return self._apply_rules(response)

    def _apply_rules(self, response: Any) -> Any:
        seen = set()
        for index, rule in enumerate(self.rules):
            for href in rule.link_extractor.extract_links(response):
                if href in seen:
                    continue
                seen.add(href)
                yield response.follow(
                    href, callback=self._crawl, cb_kwargs={"rule_index": index}
                )

    def _crawl(self, response: Any, rule_index: int) -> Any:
        rule = self.rules[rule_index]

        if rule.callback is not None:
            callback = (
                getattr(self, rule.callback)
                if isinstance(rule.callback, str)
                else rule.callback
            )
            result = callback(response)
            if result is not None:
                yield from result

        if rule.follow:
            yield from self._apply_rules(response)


class SitemapSpider(Spider):
    """Seed the crawl from ``sitemap.xml`` files (incl. sitemap indexes)."""

    sitemap_urls: list = []

    def start_requests(self) -> Any:
        for url in self.sitemap_urls:
            yield Request(url, callback=self._parse_sitemap)

    def _parse_sitemap(self, response: Any) -> Any:
        try:
            root = etree.fromstring((response.raw_html or "").encode("utf-8"))
        except etree.XMLSyntaxError:
            return

        is_index = etree.QName(root).localname == "sitemapindex"
        for loc in root.iter("{*}loc"):
            url = (loc.text or "").strip()
            if not url:
                continue
            if is_index:
                yield Request(url, callback=self._parse_sitemap)
            else:
                yield Request(url, callback=self.parse)
