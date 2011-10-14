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
    
    def __init__(self, url):
        
        self.url = url
    
    def scrape(self, html):        
        """ Define the data you want to extract here """
        
        pass
        
    def get_urls(self, html):
        """ Return a list of urls in the current html """
        
        return []
        
