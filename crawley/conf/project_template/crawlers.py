from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class %(project_name)sScraper(BaseScraper):
    
    matching_urls = ["%%www.google.com%%"]
    
    def scrape(self, html):
                
        data = html.xpath("//html/body/center/div[2]/div/font/a")
        if data:
            %(project_name)sClass(%(project_name)s_attribute=data[0].text)


class %(project_name)sCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [%(project_name)sScraper]
    max_depth = 1
    extractor = XPathExtractor 
