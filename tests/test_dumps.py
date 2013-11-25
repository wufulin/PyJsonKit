#encoding=utf-8

__author__ = 'wufulin'

import unittest
import math
import JsonParser


class TestDumps(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser.JsonParser()

    def tearDown(self):
        self.parser = None

    def test_float(self):
        for num in [1617161771.7650001, math.pi, math.pi ** 100, math.pi ** -100]:
            self.assertEqual(float(self.parser.dump(num)), num)

    def test_int(self):
        for num in [1, 1L, 1 << 32, 1 << 64]:
            self.assertEqual(self.parser.dump(num), str(num))
            self.assertEqual(int(self.parser.dump(num)), num)

    def test_truefalse(self):
        self.assertEqual(self.parser.dump(True), 'true')
        self.assertEqual(self.parser.dump(False), 'false')

    def test_none(self):
        self.assertEqual(self.parser.dump(None), 'null')

    def test_string(self):
        pass

    def test_list(self):
        print(self.parser.dump([]))
        print(self.parser.dump([2]))
        print(self.parser.dump([2, 3]))
        print(self.parser.dump([2, [2, 3]]))
        print(self.parser.dump([2, []]))
        print(self.parser.dump([False, [True, 3]]))
        print(self.parser.dump((2, [True, [False, (4, 5)]], 4)))

    def test_dict(self):
        print(self.parser.dump({}))
        print(self.parser.dump({"abc": True}))

if __name__ == '__main__':
    unittest.main()