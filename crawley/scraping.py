"""A modern, ergonomic scraping API.

This is the high level entry point for "just scrape this page" use cases. It
sits on top of the same ``httpx`` + ``lxml`` stack used by the crawler but
gives you a friendly, ``parsel``/``requests-html`` flavoured interface::

    from crawley.scraping import fetch

    doc = fetch("https://quotes.toscrape.com/")
    print(doc.css_first("h1").text)
    print(doc.css("span.text::text"))
    print(doc.links())

    rows = doc.extract({
        "quote": "span.text::text",
        "author": "small.author::text",
        "tags": ["a.tag::text"],
    })

Selectors accept an optional ``::text`` or ``::attr(name)`` suffix (just like
scrapy / parsel) to pull the text or an attribute instead of the element.
"""

from __future__ import annotations

import asyncio
import re
from typing import Any, Optional, Union

import httpx
import lxml.html

from crawley import config

__all__ = [
    "Element",
    "Document",
    "fetch",
    "afetch",
    "afetch_all",
    "scrape",
    "parse",
]

#: A value yielded by a selector: an :class:`Element` or a plain string.
Selected = Union["Element", str]

_PSEUDO_RE = re.compile(r"^(?P<sel>.*?)::(?P<op>text|attr\((?P<name>[\w:-]+)\))$")


def _split_pseudo(selector: str) -> tuple[str, Optional[str], Optional[str]]:
    """Split ``"a::attr(href)"`` into ``("a", "attr", "href")``.

    Returns ``(css, op, name)`` where *op* is ``None``, ``"text"`` or
    ``"attr"`` and *name* is the attribute name when ``op == "attr"``.
    """
    match = _PSEUDO_RE.match(selector.strip())
    if not match:
        return selector.strip(), None, None
    if match.group("op") == "text":
        return match.group("sel").strip(), "text", None
    return match.group("sel").strip(), "attr", match.group("name")


def _node_text(node: Any) -> str:
    """Return the normalized, recursive text of an lxml node."""
    if isinstance(node, str):
        return node.strip()
    text = "".join(node.itertext())
    return re.sub(r"\s+", " ", text).strip()


class Element:
    """A thin, convenient wrapper around an ``lxml`` html element."""

    def __init__(self, node: Any, url: Optional[str] = None) -> None:
        self._node = node
        self.url = url

    # -- text / attributes ----------------------------------------------

    @property
    def text(self) -> str:
        """The normalized recursive text of the element."""
        return _node_text(self._node)

    @property
    def tag(self) -> Optional[str]:
        return getattr(self._node, "tag", None)

    def attr(self, name: str, default: Any = None) -> Any:
        """Return the *name* attribute (or *default*)."""
        if isinstance(self._node, str):
            return default
        return self._node.get(name, default)

    @property
    def attrs(self) -> dict[str, str]:
        """A dict of the element's attributes."""
        if isinstance(self._node, str):
            return {}
        return dict(self._node.attrib)

    @property
    def html(self) -> str:
        """The element serialized back to html."""
        if isinstance(self._node, str):
            return self._node
        return lxml.html.tostring(self._node, encoding="unicode")

    # -- querying --------------------------------------------------------

    def css(self, selector: str) -> list[Selected]:
        """Return the descendants matching the CSS *selector*."""
        css, op, name = _split_pseudo(selector)
        nodes = self._node.cssselect(css)
        return self._wrap(nodes, op, name)

    def css_first(self, selector: str) -> Optional[Selected]:
        """Return the first descendant matching *selector* (or ``None``)."""
        results = self.css(selector)
        return results[0] if results else None

    def xpath(self, query: str) -> list[Selected]:
        """Return the result of an XPath *query*.

        String results (e.g. ``"//a/@href"``) are returned as-is; element
        results are wrapped in :class:`Element`.
        """
        return self._wrap(self._node.xpath(query), None, None)

    def _wrap(
        self, nodes: Any, op: Optional[str], name: Optional[str]
    ) -> list[Selected]:
        results: list[Selected] = []
        for node in nodes:
            if op == "text":
                results.append(_node_text(node))
            elif op == "attr":
                results.append(
                    node if isinstance(node, str) else node.get(name)
                )
            elif isinstance(node, str):
                results.append(node)
            else:
                results.append(Element(node, url=self.url))
        return results

    def __repr__(self) -> str:
        return "<Element %s>" % (self.tag or "text")


class Document(Element):
    """A parsed html document ready to be scraped."""

    def __init__(self, html: str, url: Optional[str] = None) -> None:
        self.raw_html = html
        root = (
            lxml.html.fromstring(html)
            if html.strip()
            else lxml.html.Element("html")
        )
        if url:
            try:
                root.make_links_absolute(url)
            except ValueError:
                pass
        super().__init__(root, url=url)

    @property
    def title(self) -> Optional[str]:
        """The page ``<title>`` text, if any."""
        node = self.css_first("title")
        return node.text if isinstance(node, Element) else None

    def links(self, selector: str = "a") -> list[str]:
        """Return the (absolute, de-duplicated) hrefs found in the page."""
        seen: list[str] = []
        for el in self.css(selector):
            href = el.attr("href") if isinstance(el, Element) else None
            if href and href not in seen:
                seen.append(href)
        return seen

    def extract(
        self, rules: dict[str, Union[str, list[str]]]
    ) -> dict[str, Any]:
        """Extract a dict of fields from the document.

        *rules* maps field names to selectors. A plain string selector yields
        a single value (the first match); a one-element list selector yields
        the list of every match::

            doc.extract({
                "title": "h1::text",
                "price": "span.price::text",
                "images": ["img::attr(src)"],
            })
        """
        data: dict[str, Any] = {}
        for field, selector in rules.items():
            if isinstance(selector, (list, tuple)):
                data[field] = self._extract_many(selector[0])
            else:
                values = self._extract_many(selector)
                data[field] = values[0] if values else None
        return data

    def _extract_many(self, selector: str) -> list[Any]:
        _css, op, _name = _split_pseudo(selector)
        results = self.css(selector)
        # When no pseudo element is given, default to the text of each match.
        if op is None:
            return [r.text if isinstance(r, Element) else r for r in results]
        return results

    def __repr__(self) -> str:
        return "<Document %s>" % (self.url or "")


def parse(html: str, url: Optional[str] = None) -> Document:
    """Parse an html string into a :class:`Document`."""
    return Document(html, url=url)


def _client_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    kwargs.setdefault("follow_redirects", True)
    kwargs.setdefault("timeout", config.REQUEST_TIMEOUT)
    headers = dict(kwargs.pop("headers", {}) or {})
    headers.setdefault("User-Agent", config.MOZILLA_USER_AGENT)
    kwargs["headers"] = headers
    return kwargs


def fetch(url: str, **kwargs: Any) -> Document:
    """Fetch *url* and return a parsed :class:`Document` (synchronous)."""
    with httpx.Client(**_client_kwargs(kwargs)) as client:
        response = client.get(url)
    return Document(response.text, url=str(response.url))


async def afetch(
    url: str, client: Optional[httpx.AsyncClient] = None, **kwargs: Any
) -> Document:
    """Fetch *url* asynchronously and return a :class:`Document`."""
    if client is not None:
        response = await client.get(url)
        return Document(response.text, url=str(response.url))

    async with httpx.AsyncClient(**_client_kwargs(kwargs)) as own_client:
        response = await own_client.get(url)
    return Document(response.text, url=str(response.url))


async def afetch_all(urls: Any, **kwargs: Any) -> list[Optional[Document]]:
    """Fetch many urls concurrently, returning a list of :class:`Document`."""
    urls = list(urls)
    async with httpx.AsyncClient(**_client_kwargs(kwargs)) as client:
        responses = await asyncio.gather(
            *(client.get(url) for url in urls), return_exceptions=True
        )

    documents: list[Optional[Document]] = []
    for response in responses:
        if isinstance(response, BaseException):
            documents.append(None)
        else:
            documents.append(Document(response.text, url=str(response.url)))
    return documents


def scrape(
    url: str, rules: dict[str, Union[str, list[str]]], **kwargs: Any
) -> dict[str, Any]:
    """Fetch *url* and immediately :meth:`Document.extract` it with *rules*."""
    return fetch(url, **kwargs).extract(rules)
