from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class zarasaScraper(BaseScraper):
    
    matching_urls = ["%www.google.com%"]
    
    def scrape(self, html):
                
        data = html.xpath("//html/body/center/div[2]/div/font/a")
        if data:
            zarasaClass(zarasa_attribute=data[0].text)


class zarasaCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [zarasaScraper]
    max_depth = 1
    extractor_class = XPathExtractor 
