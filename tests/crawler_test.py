import unittest
from crawley.crawlers import BaseCrawler

from test_app.crawler import GoogleCrawler, GoogleScraper
from test_app.models import GoogleText

class CrawlerTest(unittest.TestCase):
    
    def test_requests(self):
        
        testCrawler = BaseCrawler()
        response = testCrawler._get_response("http://www.facebook.com/login.php")
        self.assertEqual(response.getcode(), 200)        
    
    def test_crawl(self):
        #TODO: make a test that crawl something
        crawler = GoogleCrawler()
        
