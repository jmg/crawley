import unittest

from crawley.utils import matcher, url_matcher, OrderedDict

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

	def test_strict_matcher(self):

		self.assertTrue(matcher("http://www.a.com", "http://www.a.com"))
		self.assertTrue(matcher("www.a.com", "http://www.a.com", False))

		self.assertFalse(matcher("patron_fruta", "http://www.a.com"))
		self.assertFalse(matcher("patron_fruta", "http://www.a.com"))

	def test_ordered_dict(self):

		od = OrderedDict()
		od['a'] = 1
		od['b'] = 2

		i = 1
		for k,v in od.iteritems():
			if i == 1:
				self.assertEquals('a', k)
				self.assertEquals(1, v)
			elif i == 2:
				self.assertEquals('b', k)
				self.assertEquals(2, v)

			i += 1

	def _test_url_matcher_with_regex(self):

		self.assertTrue(url_matcher("http://www.google.com.ar", "http://([a-z.]+)"))
		self.assertTrue(url_matcher("http://www.google.com.ar", "http://(([a-z]+.){4})"))
		self.assertTrue(url_matcher("http://www.google.com.ar", "[a-z/:.]+"))

		self.assertFalse(url_matcher("http://www.google.com.ar", "http://([a-z]+)"))
		self.assertFalse(url_matcher("http://www.google.com.ar", "http://(([a-z]+.){1})"))
		self.assertFalse(url_matcher("http://www.google.com.ar", "[a-z:.]+"))
