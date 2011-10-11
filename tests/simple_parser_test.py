import unittest
from crawley.crawlers import BaseCrawler
from crawley.simple_parser import interprete
from crawley.exceptions import TemplateSyntaxError
from crawley.extractors import XPathExtractor
from dsl_tests import settings

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        
        self.test_dsl = """my_model -> /html/body/div[5]/div/div/h1
                           my_model_2 -> /html/body/div
                           my_model_3 -> /html/body/div/span"""        
    
    def test_interprete(self):
                                    
        interprete(self.test_dsl, "test1", settings)
        
        fail_dsl = """my_model -> /html/body -> other_stuff"""
        self.assertRaises(TemplateSyntaxError, interprete, fail_dsl, "test_fail", settings)
        
        fail_dsl = """my_model = /html/body"""
        self.assertRaises(TemplateSyntaxError, interprete, fail_dsl, "test_fail", settings)
            
    def test_generated_scrapers(self):
                
        Scraper = interprete(self.test_dsl, "test2", settings)
        
        crawler = BaseCrawler()
        html = crawler._get_data("http://www.python.org/")        
                        
        Scraper().scrape(XPathExtractor().get_object(html))
