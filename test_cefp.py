# -*- coding: utf-8 -*-

import unittest
import ddt
import cefp


@ddt.ddt
class TestCEF(unittest.TestCase):
    @ddt.file_data('test_cefp.json')
    def test_parse(self, input, expected):
        if isinstance(expected, dict):
            self.assertEqual(cefp.parse(input), expected)
        else:
            self.assertRaises(__builtins__[expected], cefp.parse, input)
