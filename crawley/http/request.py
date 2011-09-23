import urllib2
import cookielib
import os

class Request(object):

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
        
        request = urllib2.Request(self.url, data, self.headers)        
        opener = urllib2.build_opener(self.cookie_handler)
        
        response = opener.open(request)
        self.cookie_handler.save_cookies()
        
        return response
        
    
class CookieHanlder(urllib2.HTTPCookieProcessor):
    
    COOKIE_FILE = "/tmp/crawley-cookie"
    
    def __init__(self, *args, **kwargs):
        
        self._jar = cookielib.LWPCookieJar(self.COOKIE_FILE)
        self._jar.load()        
        
        urllib2.HTTPCookieProcessor.__init__(self, self._jar, *args, **kwargs)        
    
    def save_cookies(self):
        
        if self._jar is not None:
            self._jar.save() 
    
