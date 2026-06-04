"""Persistent cookie handling.

Wraps a :class:`http.cookiejar.LWPCookieJar` so cookies can be persisted to
and restored from a file between runs. The underlying jar is shared with the
``httpx`` client.
"""

import os.path
import tempfile
from http.cookiejar import LWPCookieJar


class CookieHandler:
    """A cookie jar that can be saved to / loaded from a temp file."""

    COOKIES_FILE = "crawley_cookies"

    def __init__(self, cookie_file=None):
        if cookie_file is None:
            cookie_file = os.path.join(tempfile.gettempdir(), self.COOKIES_FILE)
        self.cookie_file = cookie_file
        self.jar = LWPCookieJar(self.cookie_file)

    def load_cookies(self):
        """Load cookies from the file if it exists."""
        if os.path.isfile(self.cookie_file):
            self.jar.load(ignore_discard=True, ignore_expires=True)

    def save_cookies(self):
        """Persist the cookies to the file."""
        if self.jar is not None:
            self.jar.save(ignore_discard=True, ignore_expires=True)
