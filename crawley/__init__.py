"""
crawley
~~~~~~~

A pythonic crawling / scraping framework for Python 3.

The crawling core is built on top of :mod:`asyncio` and `httpx`, providing
high concurrency without the legacy ``eventlet`` dependency.
"""

__version__ = "0.3.0"

__all__ = [
    "BaseCrawler",
    "FastCrawler",
    "OffLineCrawler",
    "BaseScraper",
    "SmartScraper",
    "XPathExtractor",
    "PyQueryExtractor",
    "CSSExtractor",
    "RawExtractor",
    "Response",
    "__version__",
]


def __getattr__(name):
    """Lazily expose the public API.

    Importing :mod:`crawley` should be cheap and must not drag in optional
    dependencies (databases, GUI, ...). The public objects are resolved on
    first access instead.
    """
    if name in ("BaseCrawler", "FastCrawler", "OffLineCrawler"):
        from crawley import crawlers

        return getattr(crawlers, name)
    if name in ("BaseScraper", "SmartScraper"):
        from crawley import scrapers

        return getattr(scrapers, name)
    if name in (
        "XPathExtractor",
        "PyQueryExtractor",
        "CSSExtractor",
        "RawExtractor",
    ):
        from crawley import extractors

        return getattr(extractors, name)
    if name == "Response":
        from crawley.http.response import Response

        return Response
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
