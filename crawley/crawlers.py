from eventlet.green import urllib2
from eventlet import GreenPool

from re import compile, match
from pyquery import PyQuery

from utils import url_matcher


class BaseCrawler(object):
    """
        Base crawler class
    """
    
    start_urls = []
    scrapers = []
    max_depth = -1
    
    _url_regex = compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
    
    def __init__(self, storage=None, session=None):
        
        self.storage = storage
        self.session = session
            
    def _get_response(self, url):

        request = urllib2.Request(url)
        opener = urllib2.build_opener()        
        
        try:            
            response = opener.open(request)
            return response
        except Exception:
            return None
    
    def _get_data(self, url):
        
        response = self._get_response(url)
        if response is None or response.getcode() != 200:
            return None
        return response.read()
    
    def _manage_scrapers(self, url, data):
        
        for Scraper in self.scrapers:
            if [pattern for pattern in Scraper.matching_urls if url_matcher(url, pattern)]:
                scraper = Scraper()
                scraper.scrape(PyQuery(data))
    
    def _save_urls(self, url, new_url):
        
        if self.storage is not None:
            self.storage(parent=url, href=new_url)
            self.session.commit()
    
    def _fetch(self, url, depth_level=0):
                                            
        data = self._get_data(url);
        if data is None:
            return
            
        self._manage_scrapers(url, data)
            
        for new_url in self.get_urls(data):
                                    
            self._save_urls(url, new_url)            
            
            if depth_level >= self.max_depth:
                return
            self.pool.spawn_n(self._fetch, new_url, depth_level + 1)
            
    def start(self):
        
        self.pool = GreenPool()
        
        for url in self.start_urls:
            self.pool.spawn_n(self._fetch, url, depth_level=0)
            
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
