from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from models import GoogleText

class GoogleScraper(BaseScraper):
    
    matching_urls = ["www.google.com"]
    
    def scrape(self, html):
                
        text = html("#als").html()
        GoogleText(text=text)


class GoogleCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]    
    scrapers = [GoogleScraper]
    max_depth = 1
    
