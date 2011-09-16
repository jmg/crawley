"""
    Tests runner
"""

import unittest

if __name__ == "__main__":
    
    tests = ["tests.crawler_test", "tests.utils_test"]
    
    test_suite = unittest.defaultTestLoader.loadTestsFromNames(tests)
    unittest.TextTestRunner(verbosity=2).run(test_suite)
