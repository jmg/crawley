from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class PackagesAuthorsScraper(BaseScraper):
    
    #The pages that have the precious data
    matching_urls = ["%pypi.python.org/pypi/%"]
    
    def scrape(self, html):
                                
        project = html.xpath("/html/body/div[5]/div/div/div[3]/h1")[0].text
        author = html.xpath("/html/body/div[5]/div/div/div[3]/ul/li/span")[0].text
        
        PackagesAuthors(project=project, author=author)
        
        
class UrlsScraper(BaseScraper):
    
    #This scraper only works on the main page
    matching_urls = ["http://pypi.python.org/pypi"]
    
    def get_urls(self, html):
                
        table = html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]
                
        urls = []
        
        for tr in table[1:-1]:
            
            td_package = tr[1]
            package_link = td_package[0]            
            
            url = "http://pypi.python.org%s" % (package_link.attrib['href'])
            urls.append(url)
            
        return urls
                

class PackagesAuthorsCrawler(BaseCrawler):
    
    #add your starting urls here    
    start_urls = ["http://pypi.python.org/pypi"]
    
    #add your scraper classes here    
    scrapers = [UrlsScraper, PackagesAuthorsScraper]
    
    #specify you maximum crawling depth level    
    max_depth = 1
    
    #select your favourite HTML parsing tool
    extractor = XPathExtractor 
    
