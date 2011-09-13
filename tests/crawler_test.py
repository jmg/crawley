import unittest
from src.crawley.crawlers import BaseCrawler

import webbrowser

class CrawlerTest(unittest.TestCase):
    
    def test_requests(self):
        
        testCrawler = BaseCrawler()
        response = testCrawler._get_response("http://www.facebook.com/login.php")
        self.assertEqual(response.getcode(), 200)
        
        f = open("url.html", "w")
        f.write(response.read())
    
