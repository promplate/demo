import unittest

from tests import test_config, test_load, test_main, test_openai


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_main))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_config))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_openai))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_load))
    return suite


def run():
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    run()
