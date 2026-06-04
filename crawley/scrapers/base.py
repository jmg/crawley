"""Base scraper class."""

import logging

from crawley.exceptions import ScraperCantParseError
from crawley.utils import url_matcher

log = logging.getLogger("crawley.scraper")


class BaseScraper:
    """User scrapers must inherit from this class.

    Implement :meth:`scrape` with the data extraction logic and define the
    ``matching_urls`` that this scraper is able to process.
    """

    matching_urls = []

    def __init__(self, settings=None):
        self.settings = settings
        self.debug = getattr(settings, "SHOW_DEBUG_INFO", True)

    def try_scrape(self, response):
        """Try to parse the html page, returning the urls it discovers."""
        try:
            self._validate(response)
            self.scrape(response)
            return self.get_urls(response)
        except ScraperCantParseError:
            return None
        except Exception as ex:  # noqa: BLE001 - delegated to error handler
            self.on_scrape_error(response, ex)
            return None

    def _validate(self, response):
        """Validate that this scraper can handle *response* before scraping."""
        for pattern in self.matching_urls:
            if url_matcher(response.url, pattern):
                if self.debug:
                    log.debug(
                        "%s matches the url %s",
                        self.__class__.__name__,
                        response.url,
                    )
                return
        self.on_cannot_scrape(response)

    # -- overridables ----------------------------------------------------

    def scrape(self, response):
        """Define the data you want to extract here."""

    def get_urls(self, response):
        """Return a list of urls found in the current html."""
        return []

    # -- events ----------------------------------------------------------

    def on_scrape_error(self, response, ex):
        """Customize the scrape error handler."""
        if self.debug:
            log.warning(
                "%s failed to extract data from %s: %s",
                self.__class__.__name__,
                response.url,
                ex,
            )

    def on_cannot_scrape(self, response):
        """Customize the can't-scrape handler."""
        raise ScraperCantParseError(
            "The scraper %s can't parse the html from %s"
            % (self.__class__.__name__, response.url)
        )
