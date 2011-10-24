from base import BaseCrawler
from crawley.http.managers import FastRequestManager

class FastCrawler(BaseCrawler):
    
    def __init__(self, *args, **kwargs):
        
        BaseCrawler.__init__(self, *args, **kwargs)
        self.request_manager = FastRequestManager()
