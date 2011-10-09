import urllib2
import time
import random
from cookies import CookieHandler

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
    
    def __init__(self):
        
        self.host_counter = HostCounterDict()
        
    def make_request(self, url, cookie_handler=None, data=None):
        """
            Acumulates a counter with the requests per host and 
            then make a Delayed Request
        """
        
        host = urllib2.urlparse.urlparse(url).netloc
                   
        count = self.host_counter.count(host)
        request = DelayedRequest(url, cookie_handler, delay=300, desviation=100)        
        
        return self.get_response(request, host)
                
    def get_response(self, request, host):
        """
            Tries [MAX_TRIES] times to get the response and
            return the response data
        """
        
        response = None
        tries = 0
        
        while tries < self.MAX_TRIES and response is None:
            
            try:
                response = self._get_response(request, host)
            except:
                pass
                
            tries += 1
            
        if response is None or response.getcode() != 200:
            return None
            
        return response.read()
    
    def _get_response(self, request, host):
    
        response = request.get_response()
        self.host_counter.increase(host)
            
        return response
        

class Request(object):
    """
        Custom request object 
    """

    USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"
    
    def __init__(self, url, cookie_handler=None):
        
        if cookie_handler is None:
           cookie_handler = CookieHanlder() 
        
        self.url = url
        self.headers = {}
        self.headers["User-Agent"] = self.USER_AGENT
        self.headers["Accept-Charset"] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
        self.headers["Accept-Language"] = "es-419,es;q=0.8"
        
        self.cookie_handler = cookie_handler
    
    def get_response(self, data=None):
        """
            Returns the response object from a request.
            Cookies are supported via a CookieHandler object
        """
        
        request = urllib2.Request(self.url, data, self.headers)        
        opener = urllib2.build_opener(self.cookie_handler)
        
        response = opener.open(request)
        self.cookie_handler.save_cookies()
        
        return response


class DelayedRequest(Request):
    """
        A delayed custom Request 
    """
    
    def __init__(self, url, cookie_handler=None, delay=0, desviation=0):
        
        self.delay = delay + random.randint(-desviation, desviation)
        Request.__init__(self, url, cookie_handler)
    
    def get_response(self, data=None):
        """
            Waits [delay] miliseconds and then make the request
        """
        
        mili_seconds = self.delay / 1000
        time.sleep(mili_seconds)
        
        return Request.get_response(self, data)
