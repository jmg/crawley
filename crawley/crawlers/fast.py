"""A crawler without per-request delays."""

from crawley.crawlers.base import BaseCrawler
from crawley.http.managers import FastRequestManager


class FastCrawler(BaseCrawler):
    """Like :class:`BaseCrawler` but issues requests without delays."""

    def _make_request_manager(self):
        return FastRequestManager(
            settings=self.settings,
            headers=self.headers,
            retry_policy=self.retry_policy,
            rate_limiter=self.rate_limiter,
            cache=self._make_cache(),
        )
