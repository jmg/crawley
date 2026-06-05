"""Convenience helpers for quick, one-off requests."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Optional

from crawley.crawlers.base import BaseCrawler

if TYPE_CHECKING:
    from crawley.http.response import Response


async def async_request(url: str, data: Optional[Any] = None) -> "Response":
    """Fetch *url* (optionally POSTing *data*) and return a ``Response``."""
    crawler = BaseCrawler()
    try:
        return await crawler.request(url, data=data)
    finally:
        await crawler.request_manager.aclose()


def request(url: str, data: Optional[Any] = None) -> "Response":
    """Synchronous wrapper around :func:`async_request`."""
    return asyncio.run(async_request(url, data=data))
