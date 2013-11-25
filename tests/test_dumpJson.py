#encoding=utf-8

__author__ = 'wufulin'

import unittest
import JsonParser

FILEPATH = 'json2.txt'


class TestDumpJson(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser.JsonParser()

    def tearDown(self):
        self.parser = None

    def test_dumpJson(self):
        self.parser.dumpJson(FILEPATH, (1, 2, 3))
        self.assertEqual(self.parser.loadJson(FILEPATH), [1, 2, 3])


if __name__ == '__main__':
    unittest.main()