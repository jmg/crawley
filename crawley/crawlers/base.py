"""Base crawler class (asyncio powered)."""

import asyncio
import logging
import urllib.parse

from crawley import config
from crawley.exceptions import AuthenticationError
from crawley.extractors import XPathExtractor
from crawley.http.managers import RequestManager
from crawley.http.retry import RetryPolicy
from crawley.http.robots import RobotsPolicy
from crawley.http.throttle import HostRateLimiter
from crawley.http.urls import UrlFinder
from crawley.multiprogramming.pool import AsyncPool
from crawley.utils import url_matcher

log = logging.getLogger("crawley.crawler")

user_crawlers = []


class CrawlerMeta(type):
    """Register user crawler classes for the CLI commands.

    Abstract base crawlers (those defined inside the ``crawley`` package) are
    not registered.
    """

    def __init__(cls, name, bases, dct):
        module = getattr(cls, "__module__", "") or ""
        if not module.startswith(config.CRAWLEY_ROOT_DIR):
            user_crawlers.append(cls)
        super().__init__(name, bases, dct)


class BaseCrawler(metaclass=CrawlerMeta):
    """User crawlers must inherit from this class.

    Override the relevant methods and define ``start_urls``, ``scrapers`` and
    the ``max_depth`` to control the crawl.
    """

    start_urls = []
    """A list containing the start urls for the crawler."""

    allowed_urls = []
    """A list of url patterns allowed for crawl."""

    black_list = []
    """A list of blocked url patterns that are never crawled."""

    scrapers = []
    """A list of scraper classes."""

    max_depth = -1
    """The maximum crawling recursive level (``-1`` means unlimited)."""

    max_concurrency_level = None
    """The maximum number of concurrent requests."""

    headers = {}
    """The default request headers."""

    requests_delay = config.REQUEST_DELAY
    """The average delay time between requests."""

    requests_deviation = config.REQUEST_DEVIATION
    """The requests deviation time."""

    extractor = None
    """The extractor class. Defaults to :class:`XPathExtractor`."""

    post_urls = []
    """POST data for urls: a list of ``(url, data_dict)`` tuples."""

    login = None
    """Login data: a tuple of ``(url, login_dict)``."""

    search_all_urls = True
    """Search for urls in the page when scrapers don't return any."""

    search_hidden_urls = False
    """Search for urls hidden anywhere in the html (not only ``<a>`` tags)."""

    max_retries = config.REQUEST_MAX_RETRIES
    """How many times a failed request is retried."""

    retry_backoff = config.RETRY_BACKOFF_FACTOR
    """Base seconds for the exponential retry backoff."""

    retry_statuses = config.RETRY_STATUSES
    """HTTP status codes that trigger a retry."""

    respect_robots = config.RESPECT_ROBOTS
    """When ``True`` the crawler honours each site's ``robots.txt``."""

    crawl_delay = config.CRAWL_DELAY
    """Minimum seconds between two requests to the same host."""

    max_concurrency_per_host = config.MAX_CONCURRENCY_PER_HOST
    """Maximum simultaneous requests per host (``None`` disables the limit)."""

    unique_urls = True
    """Skip urls that have already been visited during the crawl."""

    render_js = False
    """Render pages with a headless browser (Playwright). Needs ``crawley[js]``."""

    playwright_options = {}
    """Extra options for the Playwright manager (browser_type, headless, ...)."""

    def __init__(self, sessions=None, settings=None):
        self.sessions = sessions if sessions is not None else []
        self.debug = getattr(settings, "SHOW_DEBUG_INFO", True)
        self.settings = settings
        self._seen = set()

        extractor_class = self.extractor or XPathExtractor
        self.extractor = extractor_class()

        if self.max_concurrency_level is None:
            self.max_concurrency_level = getattr(
                settings, "MAX_CONCURRENCY", config.MAX_CONCURRENCY
            )

        self.retry_policy = RetryPolicy(
            max_retries=self.max_retries,
            backoff_factor=self.retry_backoff,
            statuses=self.retry_statuses,
        )
        self.rate_limiter = HostRateLimiter(
            delay=self.crawl_delay,
            max_per_host=self.max_concurrency_per_host,
        )
        self.robots = RobotsPolicy(
            user_agent=self.headers.get("User-Agent", config.MOZILLA_USER_AGENT),
            enabled=self.respect_robots,
        )

        self.request_manager = self._make_request_manager()

        self._initialize_scrapers()

    def _make_request_manager(self):
        if self.render_js:
            from crawley.http.playwright import PlaywrightRequestManager

            return PlaywrightRequestManager(
                settings=self.settings,
                headers=self.headers,
                delay=self.requests_delay,
                deviation=self.requests_deviation,
                retry_policy=self.retry_policy,
                rate_limiter=self.rate_limiter,
                **self.playwright_options,
            )
        return RequestManager(
            settings=self.settings,
            headers=self.headers,
            delay=self.requests_delay,
            deviation=self.requests_deviation,
            retry_policy=self.retry_policy,
            rate_limiter=self.rate_limiter,
        )

    def _initialize_scrapers(self):
        self.scrapers = [
            scraper_class(settings=self.settings)
            for scraper_class in self.scrapers
        ]

    # -- requests --------------------------------------------------------

    async def _make_request(self, url, data=None):
        return await self.request_manager.make_request(url, data, self.extractor)

    async def _get_response(self, url, data=None):
        for pattern, post_data in self.post_urls:
            if url_matcher(url, pattern):
                data = post_data

        return await self._make_request(url, data)

    async def request(self, url, data=None):
        return await self._get_response(url, data=data)

    # -- scraping --------------------------------------------------------

    def _manage_scrapers(self, response):
        """Delegate the data extraction to the matching scrapers."""
        scraped_urls = []

        for scraper in self.scrapers:
            urls = scraper.try_scrape(response)
            if urls is not None:
                self._commit()
                scraped_urls.extend(urls)

        return scraped_urls

    def _commit(self):
        for session in self.sessions:
            session.commit()

    # -- url validation --------------------------------------------------

    def _search_in_urls_list(self, urls_list, url, default=True):
        if not urls_list:
            return default
        return any(url_matcher(url, pattern) for pattern in urls_list)

    def _validate_url(self, url):
        return self._search_in_urls_list(
            self.allowed_urls, url
        ) and not self._search_in_urls_list(self.black_list, url, default=False)

    # -- crawl -----------------------------------------------------------

    async def _fetch(self, url, depth_level=0):
        """Recursive url fetching."""
        if not self._validate_url(url):
            return

        if self.unique_urls:
            if url in self._seen:
                return
            self._seen.add(url)

        if self.respect_robots and not await self._robots_allowed(url):
            self.on_robots_blocked(url)
            return

        if self.debug:
            log.info("crawling -> %s", url)

        try:
            response = await self._get_response(url)
        except Exception as ex:  # noqa: BLE001 - delegated to error handler
            self.on_request_error(url, ex)
            return

        urls = self._manage_scrapers(response)

        if not urls:
            if self.search_all_urls:
                urls = self.get_urls(response)
            else:
                return

        if self.max_depth != -1 and depth_level >= self.max_depth:
            return

        for new_url in urls:
            self.pool.spawn(self._fetch(new_url, depth_level + 1))

    async def _robots_allowed(self, url):
        """Check robots.txt and apply its ``Crawl-delay`` for the host."""
        allowed = await self.robots.allowed(url, self.request_manager.client)
        delay = self.robots.crawl_delay(url)
        if delay:
            host = urllib.parse.urlparse(url).netloc
            self.rate_limiter.set_delay(host, delay)
        return allowed

    async def _login(self):
        """Authenticate before crawling, if ``login`` is configured."""
        if self.login is None:
            return

        url, data = self.login
        if await self._get_response(url, data) is None:
            raise AuthenticationError("Can't login")

    async def start(self):
        """Run the crawler (coroutine)."""
        self.pool = AsyncPool(self.max_concurrency_level)
        self._seen = set()

        self.on_start()
        await self._login()

        for url in self.start_urls:
            self.pool.spawn(self._fetch(url, depth_level=0))

        try:
            await self.pool.join()
        finally:
            await self.request_manager.aclose()

        self.on_finish()

    def run(self):
        """Convenience synchronous entry point."""
        asyncio.run(self.start())

    def get_urls(self, response):
        """Return the urls found in the current html page."""
        finder = UrlFinder(response, self.search_hidden_urls)
        return finder.get_urls()

    # -- events ----------------------------------------------------------

    def on_start(self):
        """Override to run code when the crawler starts."""

    def on_finish(self):
        """Override to run code when the crawler finishes."""

    def on_request_error(self, url, ex):
        """Override to customize the request error handler."""
        if self.debug:
            log.warning("Request to %s returned error: %s", url, ex)

    def on_robots_blocked(self, url):
        """Override to react when robots.txt disallows crawling *url*."""
        if self.debug:
            log.info("robots.txt disallows -> %s", url)
