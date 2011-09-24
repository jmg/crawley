from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class testScraper(BaseScraper):
    
    matching_urls = ["%www.google.com%"]
    
    def scrape(self, html):
                
        data = html.xpath("//html/body/center/div[2]/div/font/a")
        if data:
            testClass(test_attribute=data[0].text)


class testCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [testScraper]
    max_depth = 1
    extractor = XPathExtractor 
