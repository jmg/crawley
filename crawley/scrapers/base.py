"""
    User's Scrapers Base
"""
from crawley.exceptions import ScraperCantParseError
from crawley.utils import url_matcher

class BaseScraper(object):
    """
       User's Scrappers must Inherit from this class,
       implement the scrape method and define
       the urls that may be procesed by it.
    """

    matching_urls = []

    def __init__(self, settings=None):

        self.settings = settings
        self.debug = getattr(settings, 'SHOW_DEBUG_INFO', True)

    def try_scrape(self, response):
        """
            Tries to parse the html page
        """

        try:
            self._validate(response)
            self.scrape(response)
            return self.get_urls(response)

        except ScraperCantParseError, ex:
            pass

        except Exception, ex:
            self.on_scrape_error(response, ex)

    def _validate(self, response):
        """
            Override this method in order to provide more validations before the data extraction with the given scraper class
        """

        for pattern in self.matching_urls:

            if url_matcher(response.url, pattern):

                if self.debug:
                    print "%s matches the url %s" % (self.__class__.__name__, response.url)
                return

        self.on_cannot_scrape(response)

    #Overridables

    def scrape(self, response):
        """
            Define the data you want to extract here
        """

        pass

    def get_urls(self, response):
        """
            Return a list of urls in the current html
        """

        return []

    #Events section

    def on_scrape_error(self, response, ex):
        """
            Override this method to customize the scrape error handler.
        """

        if self.debug:
            print "%s failed to extract data from %s: %s" % (self.__class__.__name__, response.url, ex)

    def on_cannot_scrape(self, response):
        """
            Override this method to customize the can't scrape handler.
        """

        raise ScraperCantParseError("The Scraper %s can't parse the html from %s" % (self.__class__.__name__, response.url))
