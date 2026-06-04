"""Crawley's HTTP response object."""


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

    def __init__(self, raw_html=None, extracted_html=None, url=None, response=None):
        self.raw_html = raw_html
        self.html = extracted_html
        self.url = url
        self.response = response
        self._doc = None

        if response is not None:
            self.headers = response.headers
            self.status_code = response.status_code
        else:
            self.headers = {}
            self.status_code = None

    # Backwards compatible alias (the legacy API exposed ``code``).
    @property
    def code(self):
        return self.status_code

    @property
    def doc(self):
        """Return the body as a high level :class:`~crawley.scraping.Document`.

        Lets you scrape a crawler response with the modern, ergonomic API::

            def scrape(self, response):
                title = response.doc.css_first("h1").text
        """
        if self._doc is None:
            from crawley.scraping import Document

            self._doc = Document(self.raw_html or "", url=self.url)
        return self._doc

    def css(self, selector):
        """Shortcut for ``response.doc.css(selector)``."""
        return self.doc.css(selector)

    def css_first(self, selector):
        """Shortcut for ``response.doc.css_first(selector)``."""
        return self.doc.css_first(selector)

    def extract(self, rules):
        """Shortcut for ``response.doc.extract(rules)``."""
        return self.doc.extract(rules)

    def __repr__(self):
        return "<Response [%s] %s>" % (self.status_code, self.url)
