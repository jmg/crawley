from crawley.crawlers import BaseCrawler
from crawley.scrappers import BaseScrapper
from models import GoogleText

class GoogleScrapper(BaseScrapper):
    
    matching_urls = ["www.google.com"]
    
    def scrape(self, html):
                
        text = html("#als").html()
        GoogleText(text=text)


class GoogleCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]
    scrappers = [GoogleScrapper]
    max_depth = 0
    
