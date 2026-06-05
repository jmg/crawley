"""Scrapy-style spiders: requests with callbacks, items and pipelines.

This sits on top of :class:`~crawley.crawlers.base.BaseCrawler` (reusing its
async engine: httpx, retries, rate limiting, robots.txt, de-duplication) but
exposes the more powerful, callback-driven model::

    from crawley.spider import Spider, Request

    class BlogSpider(Spider):
        name = "blog"
        start_urls = ["https://example.com/"]

        def parse(self, response):
            for href in response.css("a.post::attr(href)"):
                yield response.follow(href, callback=self.parse_post)
            nxt = response.css_first("a.next::attr(href)")
            if nxt:
                yield response.follow(nxt)            # defaults to parse

        def parse_post(self, response):
            yield {
                "title": response.css_first("h1").text,
                "url": response.url,
            }
"""

from __future__ import annotations

import hashlib
import inspect
import logging
from typing import Any, Optional

from crawley.crawlers.base import BaseCrawler
from crawley.multiprogramming.pool import AsyncPool
from crawley.pipelines import DropItem

log = logging.getLogger("crawley.spider")


class Item(dict):
    """A scraped item. Just a ``dict`` you may subclass for clarity."""


class Request:
    """A scheduled HTTP request with a callback to process its response."""

    def __init__(
        self,
        url: str,
        callback: Any = None,
        method: str = "GET",
        data: Any = None,
        headers: Optional[dict] = None,
        meta: Optional[dict] = None,
        cb_kwargs: Optional[dict] = None,
        priority: int = 0,
        dont_filter: bool = False,
        errback: Any = None,
    ) -> None:
        self.url = url
        self.callback = callback
        self.method = method.upper()
        self.data = data
        self.headers = headers or {}
        self.meta = meta if meta is not None else {}
        self.cb_kwargs = cb_kwargs or {}
        self.priority = priority
        self.dont_filter = dont_filter
        self.errback = errback

    def replace(self, **kwargs: Any) -> "Request":
        """Return a copy of this request with some attributes replaced."""
        attrs = {
            "url": self.url,
            "callback": self.callback,
            "method": self.method,
            "data": self.data,
            "headers": self.headers,
            "meta": self.meta,
            "cb_kwargs": self.cb_kwargs,
            "priority": self.priority,
            "dont_filter": self.dont_filter,
            "errback": self.errback,
        }
        attrs.update(kwargs)
        return Request(**attrs)

    def fingerprint(self) -> str:
        """A stable fingerprint (method + url + body) used for de-duplication."""
        raw = "%s|%s|%s" % (self.method, self.url, self.data or "")
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def __repr__(self) -> str:
        return "<Request %s %s>" % (self.method, self.url)


class Spider(BaseCrawler):
    """A callback-driven spider.

    Define :meth:`parse` (the default callback) and yield :class:`Request`
    objects (or :func:`response.follow(...)`) to crawl further, and dicts /
    :class:`Item` objects to emit data.
    """

    name = "spider"

    pipelines: list = []
    """Item pipeline classes applied, in order, to every emitted item."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._pipelines = [pipe() for pipe in self.pipelines]

    # -- overridables ----------------------------------------------------

    def parse(self, response: Any) -> Any:
        """Default callback. Override to extract data and follow links."""
        return None

    def start_requests(self) -> Any:
        """Yield the initial requests (defaults to ``start_urls``)."""
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def on_item(self, item: Any) -> None:
        """Called for every item that survives the pipelines."""

    # -- engine ----------------------------------------------------------

    async def start(self) -> None:
        self.pool = AsyncPool(self.max_concurrency_level)
        self._seen = set()

        self.on_start()
        for pipe in self._pipelines:
            pipe.open_spider(self)

        await self._login()

        for request in self.start_requests():
            self._schedule(request, depth=0)

        try:
            await self.pool.join()
        finally:
            await self.request_manager.aclose()

        for pipe in self._pipelines:
            pipe.close_spider(self)
        self.on_finish()

    def _schedule(self, request: Request, depth: int) -> None:
        # The engine is authoritative over depth (meta may be inherited via
        # response.follow, carrying the parent's depth).
        request.meta["depth"] = depth

        if not self._validate_url(request.url):
            return

        if not request.dont_filter and self.unique_urls:
            fingerprint = request.fingerprint()
            if fingerprint in self._seen:
                return
            self._seen.add(fingerprint)

        self.pool.spawn(self._handle(request))

    async def _handle(self, request: Request) -> None:
        url = request.url

        if self.respect_robots and not await self._robots_allowed(url):
            self.on_robots_blocked(url)
            return

        if self.debug:
            log.info("crawling -> %s", url)

        try:
            response = await self.request_manager.make_request(
                url,
                data=request.data,
                extractor=self.extractor,
                headers=request.headers,
            )
        except Exception as ex:  # noqa: BLE001 - routed to the errback/handler
            self._handle_error(request, ex)
            return

        response.request = request
        callback = request.callback or self.parse
        await self._drive_callback(callback, response)

    async def _drive_callback(self, callback: Any, response: Any) -> None:
        depth = response.meta.get("depth", 0)
        cb_kwargs = response.request.cb_kwargs if response.request else {}
        result = callback(response, **cb_kwargs)

        if result is None:
            return

        if inspect.isasyncgen(result):
            async for out in result:
                await self._handle_output(out, depth)
        elif inspect.iscoroutine(result):
            res = await result
            for out in self._as_iterable(res):
                await self._handle_output(out, depth)
        else:
            for out in self._as_iterable(result):
                await self._handle_output(out, depth)

    @staticmethod
    def _as_iterable(value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, (dict, Request)):
            return [value]
        if hasattr(value, "__iter__"):
            return value
        return [value]

    async def _handle_output(self, out: Any, depth: int) -> None:
        if isinstance(out, Request):
            if self.max_depth != -1 and depth >= self.max_depth:
                return
            self._schedule(out, depth=depth + 1)
        else:
            await self._process_item(out)

    async def _process_item(self, item: Any) -> None:
        try:
            for pipe in self._pipelines:
                res = pipe.process_item(item, self)
                item = await res if inspect.iscoroutine(res) else res
        except DropItem:
            return
        self.on_item(item)

    def _handle_error(self, request: Request, ex: Exception) -> None:
        if request.errback is not None:
            request.errback(request, ex)
        else:
            self.on_request_error(request.url, ex)
