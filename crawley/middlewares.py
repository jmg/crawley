"""Downloader middlewares.

A downloader middleware is a hook around every download performed by a
:class:`~crawley.spider.Spider`. Middlewares are applied in order on the way out
(``process_request``) and in reverse order on the way back
(``process_response`` / ``process_exception``), exactly like Scrapy.

All methods may be sync or async and are optional:

- ``process_request(request, spider)`` -> ``None`` (continue), a ``Response``
  (short-circuit the download) or a ``Request`` (reschedule it instead).
- ``process_response(request, response, spider)`` -> a ``Response`` (possibly
  replaced) or a ``Request`` (reschedule).
- ``process_exception(request, exception, spider)`` -> ``None`` (propagate), a
  ``Response`` or a ``Request``.
"""

from __future__ import annotations

from typing import Any, Optional


class DownloaderMiddleware:
    """Base class for downloader middlewares (all methods optional)."""

    def process_request(self, request: Any, spider: Any) -> Any:
        return None

    def process_response(self, request: Any, response: Any, spider: Any) -> Any:
        return response

    def process_exception(
        self, request: Any, exception: Exception, spider: Any
    ) -> Optional[Any]:
        return None
