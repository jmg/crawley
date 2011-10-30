"""
    Tests runner
"""

import unittest
import sys
from optparse import OptionParser

from tests.crawler_test import CrawlerTest
from tests.utils_test import UtilsTest 
from tests.commands_test import CommandsTest
from tests.simple_parser_test import ParserTest
from tests.persistance_test import PersistanceTest

def _import_module(mod_name):
    return __import__(mod_name, globals(), locals(), ["__all__"])

def _clean_list(test_lists):
    cleaned_list = []
    for test_list in test_lists:    
        for test in test_list:
            cleaned_list.append(test)
    return cleaned_list

def get_all_tests():
    modulo_tests = _import_module('tests')
    all_tests_names = [_import_module('tests.%s' % module) for module in modulo_tests.__all__]
    test_lists = [get_tests_for(test_name) for test_name in all_tests_names]        
    return _clean_list(test_lists)

def load_tests(tests):
    
    suite = unittest.TestSuite()
    for test_class in tests:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
    
def get_tests_for(modulo):
    return ['%s.%s' % (modulo.__name__, m) for m in getattr(modulo, '__all__', [])]
    
def suite(options):
    
    if options.all is not None:
        tests = get_all_tests()
    elif options.module is not None:
        modulo = _import_module("tests.%s" % options.module)
        tests = get_tests_for(modulo)
    elif options.unittests is not None:
        return load_tests([UtilsTest, ParserTest, PersistanceTest])
    elif options.integration is not None:
        return load_tests([CommandsTest, CrawlerTest])
    else:   
        return None
    return unittest.defaultTestLoader.loadTestsFromNames(tests)

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("-i", "--integration", help="run integration tests", nargs=0)
    parser.add_option("-u", "--unittests", help="run unit tests", nargs=0)
    parser.add_option("-m", "--module", help="run tests from a specific module")
    parser.add_option("-a", "--all", help="run all tests", nargs=0)
    (options, args) = parser.parse_args()
    test_suite = suite(options)
    if len(sys.argv) <= 1 or len(sys.argv) >= 3 or test_suite is None:
        print parser.print_help()
    else:
        unittest.TextTestRunner(verbosity=2).run(test_suite)
    
