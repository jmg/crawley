import time
import random

from eventlet.green import urllib2
from cookies import CookieHandler
from crawley.manager.utils import has_valid_attr

from crawley import config


class Request(object):
    """
        Custom request object
    """

    def __init__(self, url, cookie_handler=None, settings=None):

        if cookie_handler is None:
           cookie_handler = CookieHandler()

        self.url = url
        self.headers = {}
        self.headers["User-Agent"] = config.MOZILLA_USER_AGENT
        self.headers["Accept-Charset"] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
        self.headers["Accept-Language"] = "es-419,es;q=0.8"

        self.cookie_handler = cookie_handler
        self.settings = settings

    def get_response(self, data=None, delay_factor=1):
        """
            Returns the response object from a request.
            Cookies are supported via a CookieHandler object
        """
   
        """The proxy settings is used as the following dictionary"""
        
        
        if has_valid_attr(self.settings,'PROXY_HOST') and has_valid_attr(self.settings,'PROXY_PORT'):
            
            proxy_info = {        #proxy information
            'user' : getattr(self.settings,'PROXY_USER',''),
            'pass' : getattr(self.settings,'PROXY_PASS',''),
            'host' : getattr(self.settings,'PROXY_HOST',''), #localhost
            'port' : getattr(self.settings,'PROXY_PORT',80)
            }    
            
            # build a new opener that uses a proxy requiring authorization
            proxy= urllib2.ProxyHandler({"http" :"http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
                    
            """Note: if the other method fails try this snipplet"""
            """proxy = urllib2.ProxyHandler()
            proxy.add_password(realm=None,
                                uri={'http':"http://%(user)s:%(pass)s/" % proxy_info},
                                user=proxy_info['user'],
                                passwd=proxy_info['pass'])"""
            opener = urllib2.build_opener(proxy,self.cookie_handler)
        else:
            opener = urllib2.build_opener(self.cookie_handler)
            
        self._normalize_url()

        request = urllib2.Request(self.url, data, self.headers)
        
        #install globally so it can be used with urlopen.
        #urllib2.install_opener(opener)
    
        args = {}
        if config.REQUEST_TIMEOUT is not None:
            args["timeout"] = config.REQUEST_TIMEOUT

        response = opener.open(request, **args)
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

    def __init__(self, url, cookie_handler=None, settings=None, delay=0, deviation=0):

        FACTOR = 1000.0

        deviation = deviation * FACTOR
        randomize = random.randint(-deviation, deviation) / FACTOR

        self.delay = delay + randomize
        Request.__init__(self, url, cookie_handler)

    def get_response(self, data=None, delay_factor=1):
        """
            Waits [delay] miliseconds and then make the request
        """
        delay = self.delay * delay_factor
        time.sleep(delay)
        return Request.get_response(self, data)
