"""
    Tests runner
"""

import unittest
from tests.crawler_test import CrawlerTest
from tests.utils_test import UtilsTest 
from tests.commands_test import CommandsTest
from tests.simple_parser_test import ParserTest
from tests.persistance_test import PersistanceTest

def load_tests(tests):
    
    suite = unittest.TestSuite()
    for test_class in tests:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

if __name__ == "__main__":
    
    tests = (UtilsTest, CommandsTest, PersistanceTest, CrawlerTest)
    suite = load_tests(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
