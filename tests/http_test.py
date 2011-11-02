import unittest
import os
from crawley.http.cookies import CookieHandler


class HTTPTest(unittest.TestCase):
        
    def test_cookies(self):
        """
            Test cookies dir
        """
        
        handler = CookieHandler()                
        self.assertTrue(isinstance(handler.cookie_file, basestring))
    
