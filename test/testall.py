"""Run all python test suites"""
import unittest

import testgearset

def function_suite():
    suite = unittest.TestSuite()
    suite.addTest(testgearset.TestGearSet())
    return suite

def main():
    """main() function"""
    runner = unittest.TextTestRunner()
    test_suite = function_suite()
    runner.run(test_suite)

if __name__ == "__main__":
    main()
