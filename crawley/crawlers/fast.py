"""A crawler without per-request delays."""

from crawley.crawlers.base import BaseCrawler
from crawley.http.managers import FastRequestManager


class FastCrawler(BaseCrawler):
    """Like :class:`BaseCrawler` but issues requests without delays."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_manager = FastRequestManager(
            settings=self.settings, headers=self.headers
        )
