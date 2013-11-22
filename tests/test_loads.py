#encoding=utf-8

__author__ = 'wufulin'

import unittest
import JsonParser


class TestLoads(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser.JsonParser()

    def tearDown(self):
        self.parser = None

    def test_float(self):
        pass

    def test_int(self):
        pass

if __name__ == '__main__':
    unittest.main()