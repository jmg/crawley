import unittest
from crawley.simple_parser import interprete
from crawley.simple_parser.parsers import SyntaxError

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
            
