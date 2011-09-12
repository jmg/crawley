import unittest
from src.crawley.crawlers import BaseCrawler

class CrawlerTest(unittest.TestCase):
    
    def test_requests(self):
        
        testCrawler = BaseCrawler()
        response = testCrawler._get_response("http://www.facebook.com")
        self.assertEqual(response.getcode(), 200)
    
