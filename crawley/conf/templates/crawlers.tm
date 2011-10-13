from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class %(project_name)sScraper(BaseScraper):
    
    #specify the urls that can be scraped by this class
    #example: ["%%python.org%%"] #(where %% is a wildcard)
    matching_urls = []
    
    def scrape(self, html):
                
        #parse the html and populate your model's tables here.
        #example:   
        #   data = html.xpath("//html/body/center/div[2]/div/")
        #   ModelClass(text=data[0].text)
        pass


class %(project_name)sCrawler(BaseCrawler):
    
    #add your starting urls here
    #example: ["http://packages.python.org/crawley/"]
    start_urls = []
    
    #add your scraper classes here
    #example: [%(project_name)sScraper]
    scrapers = []
    
    #specify you maximum crawling depth level    
    max_depth = 1
    
    #select your favourite HTML parsing tool
    extractor = XPathExtractor 
