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

    def __repr__(self):
        return "<Response [%s] %s>" % (self.status_code, self.url)
