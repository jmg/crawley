import unittest
from crawley.crawlers import BaseCrawler

import urllib

class CrawlerTest(unittest.TestCase):
    
    def _test_requests(self):
        """
            Very basic and foolish test
        """
        testCrawler = BaseCrawler()
        response = testCrawler._get_response("https://github.com/jmg")
        self.assertEqual(response.getcode(), 200)        
    
    def test_cookies(self):
        """
            This test asserts if the login was successful and the second request retrieves 
            a facebook's page that requires to be logged in.
        """
        testCrawler = BaseCrawler()        
        data = urllib.urlencode({'email' : 'jm_elektro@hotmail.com', 'pass': 'manchita'})
        
        response = testCrawler._get_response("https://www.facebook.com/login.php?login_attempt=1", data)
        response = testCrawler._get_response("http://www.facebook.com/profile.php?id=1271577281")
        with open("url.html", 'w') as f:
            f.write(response.read())
