import unittest

from crawley.utils import url_matcher

class UtilsTest(unittest.TestCase):

    def test_url_matcher(self):

        self.assertTrue(url_matcher("http://www.google.com.ar", "%www.google.com%"))
        self.assertTrue(url_matcher("http://www.google.com.ar", "http://www.google.com%"))
        self.assertTrue(url_matcher("http://www.google.com.ar", "%www.google.com.ar"))
        self.assertTrue(url_matcher("http://www.google.com.ar", "http://www.google.com.ar"))

        self.assertFalse(url_matcher("http://www.google.com.ar", "%www.google.com"))
        self.assertFalse(url_matcher("http://www.google.com.ar", "www.google.com%"))
        self.assertFalse(url_matcher("http://www.google.com.ar", "%www.goo.com%"))
        self.assertFalse(url_matcher("http://www.google.com.ar", "http://www.goo.com.ar"))

    def _test_url_matcher_with_regex(self):

        self.assertTrue(url_matcher("http://www.google.com.ar", "http://([a-z.]+)"))
        self.assertTrue(url_matcher("http://www.google.com.ar", "http://(([a-z]+.){4})"))
        self.assertTrue(url_matcher("http://www.google.com.ar", "[a-z/:.]+"))

        self.assertFalse(url_matcher("http://www.google.com.ar", "http://([a-z]+)"))
        self.assertFalse(url_matcher("http://www.google.com.ar", "http://(([a-z]+.){1})"))
        self.assertFalse(url_matcher("http://www.google.com.ar", "[a-z:.]+"))



