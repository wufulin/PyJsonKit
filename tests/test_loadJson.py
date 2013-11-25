#encoding=utf-8

__author__ = 'wufulin'

import unittest
import JsonParser
import os

FILENAME = "json1.txt"

class TestLoadJson(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser.JsonParser()

    def tearDown(self):
        self.parser = None

    def test_loadJson(self):
        for filePath in os.listdir(os.getcwd()):
            if filePath == 'json1.txt':
                print(self.parser.loadJson(filePath))

if __name__ == '__main__':
    unittest.main