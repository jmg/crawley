from crawley.crawlers import BaseCrawler

class GoogleCrawler(BaseCrawler):
    
    start_urls = ["http://www.google.com"]
    max_depth = 0
