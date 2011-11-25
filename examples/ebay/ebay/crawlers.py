from crawley.crawlers import BaseCrawler
from crawley.extractors import XPathExtractor
from models import *
from crawley.scrapers.smart import SmartScraper

class ebayScraper(SmartScraper):

    #specify the urls that can be scraped by this class
    #example: ["%python.org%"] #(where % is a wildcard)
    matching_urls = ["http://www.ebay.com/itm/%"]
    template_url = "http://www.ebay.com/itm/Notebook-Journal-72-pages-hand-made-Lokta-paper-/120814141537?pt=LH_DefaultDomain_0&hash=item1c21158061#ht_2348wt_1398"

    def scrape(self, response):

        #parse the html and populate your model's tables here.
        #example:
        data = response.html.xpath("/html/body/div/table/tr/td/div/table/tr/td[2]/form/table/tr/td/div/b/h1")
        ebayClass(data[0].text)


class ebayCrawler(BaseCrawler):

    #add your starting urls here
    #example: ["http://packages.python.org/crawley/"]
    start_urls = ["http://www.ebay.com/sch/Blank-Diaries-Journals-/45112/i.html?_catref=1&_trksid=p3910.c0.m449"]
    allowed_urls= ["http://www.ebay.com/%"]

    #add your scraper classes here
    #example: [ebayScraper]
    scrapers = [ebayScraper]

    #specify you maximum crawling depth level
    max_depth = 1

    #select your favourite HTML parsing tool
    extractor = XPathExtractor
