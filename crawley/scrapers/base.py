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
    
    def __init__(self, debug=False):
        
        self.debug = debug        

    def try_scrape(self, response):
        """ 
            Tries to parse the html page
        """
                        
        try:
            self._validate(response)
            self.scrape(response)
            return self.get_urls(response)
            
        except ScraperCantParseError, e:
            if self.debug:
                print "%s" % e
                
        except Exception, e:            
            if self.debug:
                print "Failed to extract data from %s: %s" % (response.url, str(e))
                                                            
    def _validate(self, response):
        """
            Override this method in order to provide more validations before the data extraction with the given scraper class
        """
        
        if self.debug:
            print "Checking response of %s is valid to matching urls of the scrapper class %s" % (response.url, self.__class__.__name__)                
                
        for pattern in self.matching_urls:
            if url_matcher(response.url, pattern):
                return
        
        raise ScraperCantParseError("The Scraper %s can't parse the html from %s" % (self.__class__.__name__, response.url))        

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
