from re import compile as re_compile
from urllib2 import urlparse

from crawley.extractors import XPathExtractor

class UrlFinder(object):
    """
        This class will find for urls in htmls
    """
    
    _url_regex = re_compile(r'(http://|https://)([a-zA-Z0-9]+\.[a-zA-Z0-9\-]+|[a-zA-Z0-9\-]+)\.[a-zA-Z\.]{2,6}(/[a-zA-Z0-9\.\?=/#%&\+-]+|/|)')
    
    def __init__(self, response, search_hidden_urls):
        
        self.response = response
        self.search_hidden_urls = search_hidden_urls
                
    def get_urls(self):
        """
            Returns a list of urls found in the current html page
        """                        
        
        urls = self.search_regulars()
                    
        if self.search_hidden_urls:
                        
            urls = self.search_hiddens(urls)
                    
        return urls
        
    def search_regulars(self):
        """
            Search urls inside the <A> tags
        """
        
        urls = set()
        
        tree = XPathExtractor().get_object(self.response.raw_html)
        
        for link_tag in tree.xpath("//a"):

            if not 'href' in link_tag.attrib:
                continue

            url = link_tag.attrib["href"]
                                    
            if not urlparse.urlparse(url).netloc:
                
                url = self._fix_url(url)

            url = self._normalize_url(url)

            urls.add(url)        
        
        return urls
        
    def _fix_url(self, url):
        """
            Fix relative urls 
        """
        
        parsed_url = urlparse.urlparse(self.response.url)
                
        if not url.startswith("/"):
             url = "/%s" % url
             
        url = "%s://%s%s" % (parsed_url.scheme, parsed_url.netloc, url)
        
        return url        
        
    def _normalize_url(self, url):
        """
            Try to normalize some weird urls
        """
        
        SLASHES = "//"
        
        if url.startswith(SLASHES):
            
            return url.replace(SLASHES, "http://")
            
        return url

    def search_hiddens(self, urls):
        """
            Search in the entire html via a regex
        """
        
        for url_match in self._url_regex.finditer(response.raw_html):
                
            urls.add(url_match.group(0))
            
        return urls
