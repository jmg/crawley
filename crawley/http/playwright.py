"""JavaScript rendering via Playwright.

A drop-in :class:`~crawley.http.managers.RequestManager` that downloads pages
with a real (headless) browser, so client-side rendered / SPA sites can be
scraped. Playwright is imported lazily and is an optional dependency::

    pip install "crawley[js]"
    playwright install chromium

Enable it on a crawler/spider with ``render_js = True``.
"""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import urlparse

from crawley.http.managers import RequestManager
from crawley.http.response import Response


class _RenderResult:
    """Minimal stand-in for an httpx response (status_code + headers)."""

    def __init__(self, status_code: Optional[int]) -> None:
        self.status_code = status_code
        self.headers: dict = {}


class PlaywrightRequestManager(RequestManager):
    """Render pages with Playwright instead of plain HTTP."""

    def __init__(
        self,
        *args: Any,
        browser_type: str = "chromium",
        headless: bool = True,
        wait_until: str = "load",
        wait_for: Optional[str] = None,
        nav_timeout: float = 30000,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.browser_type = browser_type
        self.headless = headless
        self.wait_until = wait_until
        self.wait_for = wait_for
        self.nav_timeout = nav_timeout
        self._pw = None
        self._browser = None
        self._context = None

    async def _ensure_browser(self) -> None:
        if self._browser is not None:
            return
        from playwright.async_api import async_playwright

        self._pw = await async_playwright().start()
        browser_launcher = getattr(self._pw, self.browser_type)
        self._browser = await browser_launcher.launch(headless=self.headless)
        self._context = await self._browser.new_context(
            extra_http_headers=self.headers or {}
        )

    async def _render(self, url: str, headers: Optional[dict] = None):
        """Open *url* in a fresh page and return (html, final_url, status)."""
        await self._ensure_browser()
        page = await self._context.new_page()
        try:
            if headers:
                await page.set_extra_http_headers(headers)
            nav = await page.goto(
                url, wait_until=self.wait_until, timeout=self.nav_timeout
            )
            if self.wait_for:
                await page.wait_for_selector(self.wait_for, timeout=self.nav_timeout)
            html = await page.content()
            status = nav.status if nav is not None else None
            return html, page.url, status
        finally:
            await page.close()

    async def _render_with_retry(self, url: str, headers: Optional[dict]):
        attempt = 0
        while True:
            try:
                return await self._render(url, headers)
            except Exception as ex:  # noqa: BLE001 - decided by the retry policy
                if self.retry_policy.should_retry(attempt, exception=ex):
                    await self.retry_policy.sleep(
                        self.retry_policy.backoff_time(attempt)
                    )
                    attempt += 1
                    continue
                raise

    async def make_request(
        self, url: str, data: Any = None, extractor: Any = None, headers: Any = None
    ) -> Response:
        if self.cache is not None:
            cached = self.cache.get("GET", url, data)
            if cached is not None:
                return self._response_from_cache(cached, extractor)

        import time

        host = urlparse(url).netloc
        semaphore = self.rate_limiter.semaphore(host)
        if semaphore is not None:
            await semaphore.acquire()
        try:
            await self.rate_limiter.throttle(host)
            started = time.monotonic()
            raw_html, final_url, status = await self._render_with_retry(url, headers)
            latency = time.monotonic() - started
        finally:
            if semaphore is not None:
                semaphore.release()

        if self.cache is not None:
            self.cache.store("GET", url, data, status, final_url, {}, raw_html)

        extracted = extractor.get_object(raw_html) if extractor is not None else None
        result = Response(
            raw_html=raw_html,
            extracted_html=extracted,
            url=final_url,
            response=_RenderResult(status),
        )
        result.latency = latency
        return result

    async def aclose(self) -> None:
        if self._context is not None:
            await self._context.close()
            self._context = None
        if self._browser is not None:
            await self._browser.close()
            self._browser = None
        if self._pw is not None:
            await self._pw.stop()
            self._pw = None
        self.cookie_handler.save_cookies()
