"""Convenience helpers for quick, one-off requests."""

import asyncio

from crawley.crawlers.base import BaseCrawler


async def async_request(url, data=None):
    """Fetch *url* (optionally POSTing *data*) and return a ``Response``."""
    crawler = BaseCrawler()
    try:
        return await crawler.request(url, data=data)
    finally:
        await crawler.request_manager.aclose()


def request(url, data=None):
    """Synchronous wrapper around :func:`async_request`."""
    return asyncio.run(async_request(url, data=data))
