import os.path
import urllib2
import cookielib
    
class CookieHandler(urllib2.HTTPCookieProcessor):
    """
        Cookie jar wrapper for save and load cookie from a file
    """
    
    COOKIE_FILE = "/tmp/crawley_cookie"
    
    def __init__(self, *args, **kwargs):        
                
        self._jar = cookielib.LWPCookieJar(self.COOKIE_FILE)
        self.load_cookies()
        
        urllib2.HTTPCookieProcessor.__init__(self, self._jar, *args, **kwargs)        
    
    def load_cookies(self):
        """
            Load cookies from the file
        """
        
        if os.path.isfile(self.COOKIE_FILE):
            self._jar.load()
    
    def save_cookies(self):
        """
            Save cookies if the jar is not empty
        """
        
        if self._jar is not None:
            self._jar.save() 
