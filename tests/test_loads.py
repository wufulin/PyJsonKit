#encoding=utf-8

__author__ = 'wufulin'

import unittest
import JsonParser

jsonTest = r'''[
    "JSON Test Pattern pass1",
    {"object with 1 member":["array with 1 element"]},
    {},
    [],
    -42,
    true,
    false,
    null,
    {"integer": 1234567890,"real": -9876.543210,"e": 0.123456789e-12}
    ]
    '''

class TestLoads(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser.JsonParser()

    def tearDown(self):
        self.parser = None

    def test_number(self):
        self.assertEqual(self.parser.load('-23'), -23)
        self.assertEqual(self.parser.load('-0.2'), -0.2)
        self.assertEqual(self.parser.load('-23.07'), -23.07)
        self.assertEqual(self.parser.load('-23.07E-4'), -0.002307)
        self.assertEqual(self.parser.load('-23.07E+4'), -230700)

    def test_null(self):
        self.assertEqual(self.parser.load('null'), None)
        self.assertEqual(self.parser.load('   null'), None)

    def test_false(self):
        self.assertEqual(self.parser.load('false'), False)
        self.assertEqual(self.parser.load('     false   '), False)

    def test_true(self):
        self.assertEqual(self.parser.load('true'), True)
        self.assertEqual(self.parser.load('     true'), True)

    def test_array(self):
        self.assertEqual(self.parser.load('[true,false]'), [True, False])
        self.assertEqual(self.parser.load('[  true,   false  ]'), [True, False])
        self.assertEqual(self.parser.load('[ ]'), [])
        self.assertEqual(self.parser.load('[1,2,3]'), [1, 2, 3])
        self.assertEqual(self.parser.load('[[[[null]]]]'), [[[[None]]]])

    def test_string(self):
        self.assertEqual(self.parser.load('"abc"'), u'abc')
        self.assertEqual(self.parser.load('""'), u'')
        self.assertEqual(self.parser.load('"\\tabc"'), u'\tabc')
        self.assertEqual(self.parser.load('"\\nabc"'), u'\nabc')
        self.assertEqual(self.parser.load('"\\u1223"'), u'\u1223')

    def test_object(self):
        print(self.parser.load(jsonTest))
        print(self.parser.load('{"name":[456, "b", "c"]}'))
        self.assertEqual(self.parser.load('{"name":"wufulin"}'), {u'name': u'wufulin'})
        self.assertEqual(self.parser.load('{"name":["a", "b", "c"]}'), {u'name': ['a', 'b', 'c']})
        self.assertEqual(self.parser.load('{"name":"wufulin", "class":"one"}'), {u'name': u'wufulin', u'class': u'one'})
        self.assertEqual(self.parser.load('{}'), {})
        self.assertEqual(self.parser.load('{"name":{"sex":"female"}}'), {"name": {"sex": "female"}})

if __name__ == '__main__':
    unittest.main()