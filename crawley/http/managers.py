import urllib

from request import DelayedRequest, Request
from crawley.http.cookies import CookieHandler
from crawley.http.response import Response
from crawley.utils import has_valid_attr


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

    def __init__(self, settings=None, delay=None, deviation=None):

        self.host_counter = HostCounterDict()
        self.cookie_handler = CookieHandler()
        self.delay = delay
        self.deviation = deviation
        self.settings = settings
        self.proxy = self._get_proxy()
        self.request = None

    def _get_proxy(self):

        if has_valid_attr(self.settings,'PROXY_HOST') and has_valid_attr(self.settings,'PROXY_PORT'):

            proxy_info = {        #proxy information
                'user' : getattr(self.settings, 'PROXY_USER', ''),
                'pass' : getattr(self.settings, 'PROXY_PASS', ''),
                'host' : getattr(self.settings, 'PROXY_HOST', ''), #localhost
                'port' : getattr(self.settings, 'PROXY_PORT', 80)
            }

            # build a new opener that uses a proxy requiring authorization
            return {"http" :"http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info}

        return None

    def _get_request(self, url):

        return DelayedRequest(url=url, cookie_handler=self.cookie_handler, proxy=self.proxy, delay=self.delay, deviation=self.deviation)

    def make_request(self, url, data=None, extractor=None):
        """
            Acumulates a counter with the requests per host and
            then make a Delayed Request
        """

        if self.request is None:
            self.request = self._get_request(url)
        else:
            self.request.url = url

        if data is not None:
            data = urllib.urlencode(data)

        response = self.get_response(self.request, data)
        raw_html = response.text
        binary_content = response.content

        extracted_html = None

        if extractor is not None:
            extracted_html = extractor.get_object(raw_html)

        return Response(raw_html=raw_html, binary_content=binary_content, extracted_html=extracted_html, url=url, response=response)

    def get_response(self, request, data):
        """
            Tries [MAX_TRIES] times to get the response and
            return the response data
        """

        response = None
        tries = 0

        while response is None:

            try:
                response = request.get_response(data, delay_factor=tries)
            except Exception, ex:
                if tries >= self.MAX_TRIES:
                    raise ex

            tries += 1

        return response


class FastRequestManager(RequestManager):

    def _get_request(self, url):

        return Request(url=url, cookie_handler=self.cookie_handler, proxy=self.proxy)
