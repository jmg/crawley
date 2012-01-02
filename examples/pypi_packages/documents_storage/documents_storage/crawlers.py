from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class pypiScraper(BaseScraper):

    #specify the urls that can be scraped by this class
    matching_urls = ["%"]

    def scrape(self, response):

        #getting the html table
        table = response.html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]

        #for rows 1 to n-1
        for tr in table[1:-1]:

            #obtaining the searched html inside the rows
            td_updated = tr[0]
            td_package = tr[1]
            package_link = td_package[0]
            td_description = tr[2]

            data = {"updated" : td_updated.text, "package" : package_link.text, "description" : td_description.text }

            #storing data in the xml document
            XMLPackage(**data)
            #storing data in the json document
            JSONPackage(**data)
            #storing data in the csv document
            CSVPackage(**data)


class pypiCrawler(BaseCrawler):

    #add your starting urls here
    start_urls = ["http://pypi.python.org/pypi"]

    #add your scraper classes here
    scrapers = [pypiScraper]

    #specify you maximum crawling depth level
    max_depth = 0

    #select your favourite HTML parsing tool
    extractor = XPathExtractor
