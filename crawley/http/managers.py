from eventlet.green import urllib2
from request import DelayedRequest, Request

import urllib

class HostCounterDict(dict):
    """
        A counter dictionary for requested hosts 
    """
    
    def increase(self, key):
        
        if key in self:
            self[key] += 1
        else:
            self[key] = 1
            
    def count(self, key):
        
        if not key in self:
            self[key] = 0
            
        return self[key]
        

class RequestManager(object):
    """
        Manages the http requests 
    """
    
    MAX_TRIES = 3
    
    def __init__(self, delayed=True):
        
        self.host_counter = HostCounterDict()
        self.delayed = delayed
    
    def _get_request(self, url, cookie_handler=None):
        
        host = urllib2.urlparse.urlparse(url).netloc
        count = self.host_counter.count(host)
                
        return DelayedRequest(url, cookie_handler, delay=300, desviation=100)
    
    def make_request(self, url, cookie_handler=None, data=None):
        """
            Acumulates a counter with the requests per host and 
            then make a Delayed Request
        """                                
        request = self._get_request(url, cookie_handler)
        
        if data is not None:
            data = urllib.urlencode(data)
        
        return self.get_response(request, data)
                
    def get_response(self, request, data):
        """
            Tries [MAX_TRIES] times to get the response and
            return the response data
        """
        
        response = None
        tries = 0
        
        while tries < self.MAX_TRIES and response is None:
            
            try:
                response = self._get_response(request, data)
            except:
                pass
                
            tries += 1
            
        if response is None or response.getcode() != 200:
            return None
            
        return response.read()
    
    def _get_response(self, request, data):
    
        response = request.get_response(data)        
            
        return response


class FastRequestManager(RequestManager):
    
    def _get_request(self, url, cookie_handler=None):
    
        return Request(url, cookie_handler)
