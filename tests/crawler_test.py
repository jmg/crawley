import unittest
from crawley.crawlers import BaseCrawler

import urllib


class PostCrawler(BaseCrawler):
            
    start_urls = ["https://github.com/jmg"]            
    post_urls = [("https://github.com/jmg", {'user' : 'jm'})]
    max_depth = 0


class CrawlerTest(unittest.TestCase):
    
    def setUp(self):
        self.crawler = BaseCrawler() 
    
    def test_requests(self):
        """
            Very basic and foolish test
        """
        response = self.crawler._get_response("https://github.com/jmg")
        self.assertEqual(response.getcode(), 200)        
    
    def test_cookies(self):
        """
            This test asserts if the login was successful and the second request retrieves 
            a facebook's page that requires to be logged in.
        """        
        data = urllib.urlencode({'email' : 'your_user', 'pass': 'your_pass'})
        
        response = self.crawler._get_response("https://www.facebook.com/login.php?login_attempt=1", data)
        response = self.crawler._get_response("http://www.facebook.com/profile.php?id=1271577281")
        with open("url.html", 'w') as f:
            f.write(response.read())
    
    def test_post(self):
        
        crawler = PostCrawler()        
        crawler.start()
