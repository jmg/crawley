import requests


class CookieHandler(object):
    """
        Cookie jar wrapper for save and load cookie from a file
    """

    def __init__(self):
        self._jar = requests.cookies.RequestsCookieJar()

    def cookiejar_from_dict(self, cookie_dict):
        self._jar = requests.cookies.cookiejar_from_dict(cookie_dict)

    @property
    def jar(self):
        return self._jar
