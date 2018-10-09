#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import unittest
from mathfunc import *


class TestMathFunc(unittest.TestCase):

    def setUp(self):
        pass

    def test_add(self):
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(2, add(1, 2))

    def test_minus(self):
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        self.assertEqual(2, divide(6, 3))
        #self.assertEqual(2.5, divide(5, 2))

    def tearDown(self):
        pass


if __name__ == '__main__':

    test_runner = unittest.TextTestRunner()
    test_suite = unittest.TestSuite()
    test_suite.addTests(map(TestMathFunc, ['test_add', 'test_minus', 'test_multi', 'test_divide']))
    test_runner.run(test_suite)

    # unittest.main(verbosity=2)


