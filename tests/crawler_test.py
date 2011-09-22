import unittest
from crawley.crawlers import BaseCrawler


class CrawlerTest(unittest.TestCase):
    
    def test_requests(self):
        
        testCrawler = BaseCrawler()
        response = testCrawler._get_response("https://github.com/jmg")
        self.assertEqual(response.getcode(), 200)        
    
    def test_crawl(self):
        #TODO: make a test that crawl something
        pass
        
