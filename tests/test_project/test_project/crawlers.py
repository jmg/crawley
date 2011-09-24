from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class test_projectScraper(BaseScraper):
    
    matching_urls = ["%www.google.com%"]
    
    def scrape(self, html):
                
        data = html.xpath("//html/body/center/div[2]/div/font/a")
        if data:
            test_projectClass(test_project_attribute=data[0].text)


class test_projectCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [test_projectScraper]
    max_depth = 1
    extractor_class = XPathExtractor 
