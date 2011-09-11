from eventlet.green import urllib2
from eventlet import GreenPool

from re import compile, match
from pyquery import PyQuery

class BaseCrawler(object):
    
    start_urls = []
    scrappers = []
    max_depth = -1    
    
    _url_regex = compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
    
    def __init__(self, storage=None, session=None):
        
        self.storage = storage
        self.session = session
    
    def fetch(self, url, depth_level=0):
                                
        try:
            data = urllib2.urlopen(url).read()
        except Exception:
            return 
            
        for Scrapper in self.scrappers:
            if [match_url for match_url in Scrapper.matching_urls if match_url in url]:
                scrapper = Scrapper()
                scrapper.scrape(PyQuery(data))
            
        for new_url in self.get_urls(data):                        
            
            if self.storage is not None:
                self.storage(parent=url, href=new_url)
                self.session.commit()                            
            
            if depth_level > self.max_depth:
                return
            self.pool.spawn_n(self.fetch, new_url, depth_level + 1)            
            
    def start(self):
        
        self.pool = GreenPool()
        self.urls = set()
        
        for url in self.start_urls:            
            self.fetch(url, depth_level=0)
            
        self.pool.waitall()                        


    #overridables
    
    def get_urls(self, html):
        """
            Returns a list of urls found in the current html page
        """
        urls = []
        for url_match in self._url_regex.finditer(html):
            urls.append(url_match.group(0))
        return urls
        
        
