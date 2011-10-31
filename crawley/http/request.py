import time
import random

from eventlet.green import urllib2
from cookies import CookieHandler

from crawley import config


class Request(object):
    """
        Custom request object
    """

    def __init__(self, url=None, cookie_handler=None, opener=None):

        if cookie_handler is None:
           cookie_handler = CookieHandler()

        self.url = url
        self.headers = {}
        self.headers["User-Agent"] = config.MOZILLA_USER_AGENT
        self.headers["Accept-Charset"] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
        self.headers["Accept-Language"] = "es-419,es;q=0.8"

        self.cookie_handler = cookie_handler
        self.opener = opener

    def get_response(self, data=None, delay_factor=1):
        """
            Returns the response object from a request.
            Cookies are supported via a CookieHandler object
        """
   
        """The proxy settings is used as the following dictionary"""
                                    
        self._normalize_url()

        request = urllib2.Request(self.url, data, self.headers)
    
        args = {}
        if config.REQUEST_TIMEOUT is not None:
            args["timeout"] = config.REQUEST_TIMEOUT

        response = self.opener.open(request, **args)
        self.cookie_handler.save_cookies()

        return response

    def _normalize_url(self):
        """
            Normalize the request url
        """

        self.url = urllib2.quote(self.url.encode('utf-8'), safe="%/:=&?~#+!$,;'@()*[]")


class DelayedRequest(Request):
    """
        A delayed custom Request
    """

    def __init__(self, delay=0, deviation=0, **kwargs):

        FACTOR = 1000.0

        deviation = deviation * FACTOR
        randomize = random.randint(-deviation, deviation) / FACTOR

        self.delay = delay + randomize        
        Request.__init__(self, **kwargs)

    def get_response(self, data=None, delay_factor=1):
        """
            Waits [delay] miliseconds and then make the request
        """
        
        delay = self.delay * delay_factor
        time.sleep(delay)
        return Request.get_response(self, data)
