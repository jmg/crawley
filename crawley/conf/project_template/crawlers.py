from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from models import *

class %(project_name)sScraper(BaseScraper):
    
    matching_urls = ["%%www.google.com%%"]
    
    def scrape(self, html):
                
        data = html("#als").html()
        %(project_name)sClass(%(project_name)s_attribute=data)


class %(project_name)sCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [%(project_name)sScraper]
    max_depth = 1
