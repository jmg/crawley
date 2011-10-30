import urllib

from eventlet.green import urllib2
from request import DelayedRequest, Request
from crawley.http.cookies import CookieHandler
from crawley.http.response import Response
from crawley import config


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

    def _get_request(self, url):

        host = urllib2.urlparse.urlparse(url).netloc
        count = self.host_counter.count(host)

        return DelayedRequest(url, self.cookie_handler, settings=self.settings, delay=self.delay, deviation=self.deviation)

    def make_request(self, url, data=None, extractor=None):
        """
            Acumulates a counter with the requests per host and
            then make a Delayed Request
        """
        request = self._get_request(url)

        if data is not None:
            data = urllib.urlencode(data)

        response = self.get_response(request, data)
        raw_html = self._get_data(response)

        extracted_html = None

        if extractor is not None:
            extracted_html = extractor.get_object(raw_html)

        return Response(raw_html=raw_html, extracted_html=extracted_html, url=url, response=response)

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

    def _get_data(self, response):

        return response.read()


class FastRequestManager(RequestManager):

    def _get_request(self, url, cookie_handler=None):

        return Request(url, cookie_handler)
