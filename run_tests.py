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
from tests.http_test import HTTPTest


def load_tests(tests):

    suite = unittest.TestSuite()
    for test_class in tests:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

def suite(options):
    unit = [UtilsTest, ParserTest, PersistanceTest, HTTPTest]
    integration = [CommandsTest, CrawlerTest]

    if options.all is not None:
        return load_tests(unit + integration)
    elif options.unittests is not None:
        return load_tests(unit)
    elif options.integration is not None:
        return load_tests(integration)
    else:
        return None

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-i", "--integration", help="run integration tests", nargs=0)
    parser.add_option("-u", "--unittests", help="run unit tests", nargs=0)
    parser.add_option("-a", "--all", help="run all tests", nargs=0)
    (options, args) = parser.parse_args()
    test_suite = suite(options)
    if len(sys.argv) <= 1 or len(sys.argv) >= 3 or test_suite is None:
        print parser.print_help()
    else:
        unittest.TextTestRunner(verbosity=2).run(test_suite)

