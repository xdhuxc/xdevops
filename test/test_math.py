#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import unittest
from mathfunc import *

class TestMathFunc(unittest.TestCase):

    def test_add(self):
        self.assertTrue(3, add(1,2))

if __name__ == '__main__':
    unittest.main()

