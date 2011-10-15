import unittest
from crawley.crawlers import BaseCrawler
from crawley.simple_parser import interprete
from crawley.exceptions import TemplateSyntaxError
from crawley.extractors import XPathExtractor
from dsl_tests import settings

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        
        pass       
    
    def test_interprete(self):
        
        test_dsl = """table1 => http://www.python.org/
                      my_model -> /html/body/div[5]/div/div/h1
                      my_model_2 -> /html/body/div
                      my_model_3 -> /html/body/div/span""" 
                                    
        interprete(test_dsl, settings)
        
        fail_dsl = """my_model -> /html/body -> other_stuff"""
        self.assertRaises(TemplateSyntaxError, interprete, fail_dsl, settings)
        
        fail_dsl = """my_model = /html/body"""
        self.assertRaises(TemplateSyntaxError, interprete, fail_dsl, settings)
            
    def test_generated_scrapers(self):
        
        test_dsl = """table2 => http://www.python.org/
                      my_model -> /html/body/div[5]/div/div/h1
                      my_model_2 -> /html/body/div
                      my_model_3 -> /html/body/div/span""" 
                
        scrapers_classes = interprete(test_dsl, settings)
        
        crawler = BaseCrawler()
        html = crawler._get_data("http://www.python.org/")        
                
        for scraper_class in scrapers_classes:
            scraper_class(None).scrape(XPathExtractor().get_object(html))
