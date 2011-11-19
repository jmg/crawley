import os.path
import urllib2
import cookielib
import tempfile

class CookieHandler(urllib2.HTTPCookieProcessor):
    """
        Cookie jar wrapper for save and load cookie from a file
    """

    COOKIES_FILE = "crawley_cookies"

    def _make_temp_file(self):

        tmp = tempfile.gettempdir()
        self.cookie_file = os.path.join(tmp, self.COOKIES_FILE)

    def __init__(self, *args, **kwargs):

        self._make_temp_file()

        self._jar = cookielib.LWPCookieJar(self.cookie_file)
        urllib2.HTTPCookieProcessor.__init__(self, self._jar, *args, **kwargs)

    def load_cookies(self):
        """
            Load cookies from the file
        """

        if os.path.isfile(self.cookie_file):
            self._jar.load()

    def save_cookies(self):
        """
            Save cookies if the jar is not empty
        """

        if self._jar is not None:
            self._jar.save()
