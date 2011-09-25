"""
    Scrapers.py
"""

class BaseScraper(object):
    """
       User's Scrappers must Inherit from this class, 
       implement the scrape method and define 
       the urls that may be procesed by it.
    """
        
    matching_urls = []
    
    def scrape(self, html):        
        """ This method should be overwritten by user's scrapers """
        
        pass
