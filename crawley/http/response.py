"""Crawley's HTTP response object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from crawley.scraping import Document, Selected


class Response:
    """Encapsulates an HTTP response.

    Attributes:
        raw_html: the decoded body of the response (``str``).
        html: the body parsed by the crawler's extractor (lxml tree, PyQuery
            object, ...). ``None`` when no extractor was used.
        url: the final url of the request (after redirects).
        status_code: the HTTP status code.
        headers: the response headers.
    """

    def __init__(
        self,
        raw_html: Optional[str] = None,
        extracted_html: Any = None,
        url: Optional[str] = None,
        response: Any = None,
    ) -> None:
        self.raw_html = raw_html
        self.html = extracted_html
        self.url = url
        self.response = response
        self.request: Any = None
        self._doc: Optional[Document] = None

        if response is not None:
            self.headers = response.headers
            self.status_code = response.status_code
        else:
            self.headers = {}
            self.status_code = None

    # Backwards compatible alias (the legacy API exposed ``code``).
    @property
    def code(self) -> Any:
        return self.status_code

    @property
    def doc(self) -> "Document":
        """Return the body as a high level :class:`~crawley.scraping.Document`.

        Lets you scrape a crawler response with the modern, ergonomic API::

            def scrape(self, response):
                title = response.doc.css_first("h1").text
        """
        if self._doc is None:
            from crawley.scraping import Document

            self._doc = Document(self.raw_html or "", url=self.url)
        return self._doc

    def css(self, selector: str) -> "list[Selected]":
        """Shortcut for ``response.doc.css(selector)``."""
        return self.doc.css(selector)

    def css_first(self, selector: str) -> "Optional[Selected]":
        """Shortcut for ``response.doc.css_first(selector)``."""
        return self.doc.css_first(selector)

    def extract(self, rules: dict) -> dict:
        """Shortcut for ``response.doc.extract(rules)``."""
        return self.doc.extract(rules)

    @property
    def meta(self) -> dict:
        """The ``meta`` dict carried by the originating request (if any)."""
        if self.request is not None:
            return self.request.meta
        return {}

    def follow(self, url: str, callback: Any = None, **kwargs: Any) -> Any:
        """Build a :class:`~crawley.spider.Request` to a (possibly relative) url.

        Relative urls are resolved against this response's url, and ``meta`` is
        inherited from the current request unless overridden.
        """
        from urllib.parse import urljoin

        from crawley.spider import Request

        absolute = urljoin(self.url or "", url)
        if "meta" not in kwargs and self.request is not None:
            kwargs["meta"] = dict(self.request.meta)
        return Request(absolute, callback=callback, **kwargs)

    def __repr__(self) -> str:
        return "<Response [%s] %s>" % (self.status_code, self.url)
