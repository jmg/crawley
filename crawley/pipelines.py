"""Item pipelines.

A pipeline post-processes every item yielded by a :class:`~crawley.spider.Spider`
callback: validate, clean, de-duplicate or store it. Pipelines are tried in
order; raising :class:`DropItem` discards the item.
"""

from __future__ import annotations

from typing import Any


class DropItem(Exception):
    """Raise from ``process_item`` to discard the current item."""


class ItemPipeline:
    """Base class for item pipelines (all methods are optional)."""

    def open_spider(self, spider: Any) -> None:
        """Called once when the spider starts."""

    def close_spider(self, spider: Any) -> None:
        """Called once when the spider finishes."""

    def process_item(self, item: Any, spider: Any) -> Any:
        """Return the (possibly transformed) item, or raise :class:`DropItem`."""
        return item
