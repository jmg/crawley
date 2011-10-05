import unittest
from crawley.crawlers import BaseCrawler
from crawley.simple_parser import interprete
from crawley.simple_parser.parsers import SyntaxError
from crawley.extractors import XPathExtractor

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_interprete(self):
        
        test_dsl = """my_model -> /html/body"""
        interprete(test_dsl)
        
        fail_dsl = """my_model -> /html/body -> other_stuff"""
        self.assertRaises(SyntaxError, interprete, fail_dsl)
        
        fail_dsl = """my_model = /html/body"""
        self.assertRaises(SyntaxError, interprete, fail_dsl)
            
    def test_generated_scrapers(self):
        
        test_dsl = """my_model -> /html/body/div[5]/div/div/h1"""
        Scraper = interprete(test_dsl)
        
        crawler = BaseCrawler()
        html = crawler._get_data("http://www.python.org/")        
                        
        Scraper().scrape(XPathExtractor().get_object(html))
