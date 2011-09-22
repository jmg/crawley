import urllib2
import cookielib
import os

class Request(object):

    USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"
    
    def __init__(self, url):
        
        self.url = url
        self.headers = {"user_agent" : self.USER_AGENT }
    
    def get_response(self, data=None):
        
        request = urllib2.Request(self.url, data, self.headers)        
        
        self._cookie_hanlder = CookieHanlder()
        opener = urllib2.build_opener(self._cookie_hanlder)
        
        response = opener.open(request)
        self._cookie_hanlder.save_cookies()
        
        return response
        
    
class CookieHanlder(urllib2.HTTPCookieProcessor):
    
    COOKIE_FILE = "/tmp/crawley-cookie"
    
    def __init__(self, *args, **kwargs):
        
        self._jar = cookielib.LWPCookieJar()
        
        if os.path.isfile(self.COOKIE_FILE):
            self._jar.load(self.COOKIE_FILE)
        
        urllib2.HTTPCookieProcessor.__init__(self, self._jar, *args, **kwargs)
        
    
    def save_cookies(self):
        
        if self._jar is not None:
            self._jar.save(self.COOKIE_FILE) 
    
