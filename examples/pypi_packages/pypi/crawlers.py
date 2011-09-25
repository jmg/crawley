from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class pypiScraper(BaseScraper):
    
    #specify the urls that can be scraped by this class
    matching_urls = ["%"]
    
    def scrape(self, html):
                
        #parse the html and populate your model's tables here.
        table = html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]
        
        for tr in table[1:-1]:
                                       
            td_updated = tr[0]
            td_package = tr[1]
            package_link = td_package[0]
            td_description = tr[2]
            
            Package(updated=td_updated.text, package=package_link.text, description=td_description.text)


class pypiCrawler(BaseCrawler):
    
    #add your starting urls here
    start_urls = ["http://pypi.python.org/pypi"]
    
    #add your scraper classes here    
    scrapers = [pypiScraper]
    
    #specify you maximum crawling depth level    
    max_depth = 0
    
    #select your favourite HTML parsing tool
    extractor = XPathExtractor
