"""
    Scrapers.py
"""

class BaseScraper(object):
        
    matching_urls = []
    
    def scrape(self, html):
        """ This method should be overrided in user scrapers """
        pass
