"""
    User's Scrapers Base
"""

class BaseScraper(object):
    """
       User's Scrappers must Inherit from this class,
       implement the scrape method and define
       the urls that may be procesed by it.
    """

    matching_urls = []

    def scrape(self, response):
        """ Define the data you want to extract here """

        pass

    def get_urls(self, response):
        """ Return a list of urls in the current html """

        return []

