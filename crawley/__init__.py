"""
crawley
~~~~~~~

A pythonic crawling / scraping framework for Python 3.

The crawling core is built on top of :mod:`asyncio` and `httpx`, providing
high concurrency without the legacy ``eventlet`` dependency.
"""

import logging

# Library best practice: attach a no-op handler so importing crawley never
# emits "No handlers could be found" warnings. Applications configure logging.
logging.getLogger("crawley").addHandler(logging.NullHandler())

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
    "fetch",
    "afetch",
    "afetch_all",
    "scrape",
    "parse",
    "Document",
    "Element",
    "Spider",
    "Request",
    "FormRequest",
    "Item",
    "DropItem",
    "ItemPipeline",
    "LinkExtractor",
    "Rule",
    "CrawlSpider",
    "SitemapSpider",
    "StatsCollector",
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
    if name in ("Spider", "Request", "FormRequest", "Item"):
        from crawley import spider

        return getattr(spider, name)
    if name in ("DropItem", "ItemPipeline"):
        from crawley import pipelines

        return getattr(pipelines, name)
    if name in ("LinkExtractor", "Rule", "CrawlSpider", "SitemapSpider"):
        from crawley import spiders

        return getattr(spiders, name)
    if name == "StatsCollector":
        from crawley.stats import StatsCollector

        return StatsCollector
    if name in ("fetch", "afetch", "afetch_all", "scrape", "parse", "Document", "Element"):
        from crawley import scraping

        return getattr(scraping, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
