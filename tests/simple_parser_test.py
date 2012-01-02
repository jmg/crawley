import unittest
from crawley.crawlers import BaseCrawler
from crawley.simple_parser import Generator
from crawley.exceptions import TemplateSyntaxError
from crawley.extractors import XPathExtractor
from crawley.http.response import Response
from dsl_tests import settings

class ParserTest(unittest.TestCase):

    def setUp(self):

        pass

    def test_interprete(self):

        test_dsl = """PAGE => http://www.python.org/
                      table1.model1 -> /html/body/div[5]/div/div/h1
                      table1.model2 -> /html/body/div
                      table2.model1 -> /html/body/div/span"""

        fail_dsl = """my_model -> /html/body -> other_stuff"""
        self.assertRaises(TemplateSyntaxError, Generator, fail_dsl, settings)

        fail_dsl = """my_model = /html/body"""
        self.assertRaises(TemplateSyntaxError, Generator, fail_dsl, settings)

    def test_generated_scrapers(self):

        test_dsl = """PAGE => http://www.python.org/
                      table3.model1 -> /html/body/div[5]/div/div/h1
                      table3.model2 -> /html/body/div
                      table4.model1 -> /html/body/div/span"""

        generator = Generator(test_dsl, settings)
        generator.gen_entities()

        scrapers_classes = generator.gen_scrapers()

        crawler = BaseCrawler()
        response = crawler._get_response("http://www.python.org/")

        for scraper_class in scrapers_classes:
            scraper_class().scrape(response)
