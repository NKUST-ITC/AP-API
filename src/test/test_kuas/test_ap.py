import config
import unittest


class FooTest(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(1 == 1)
        self.assertTrue(config.UNITTEST_USERNAME)
