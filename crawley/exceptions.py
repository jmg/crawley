"""Crawley exceptions."""


class CrawleyError(Exception):
    """Base class for every crawley specific error."""


class AuthenticationError(CrawleyError):
    """Raised when a login attempt fails."""


class TemplateSyntaxError(CrawleyError):
    """Raised when the DSL template has a syntax error."""

    def __init__(self, line=0, *args, **kwargs):
        self.line = line
        super().__init__(*args, **kwargs)


class ScraperCantParseError(CrawleyError):
    """Raised when a scraper can't parse an html page."""


class InvalidProjectError(CrawleyError):
    """Raised when the user opens an invalid project directory."""
