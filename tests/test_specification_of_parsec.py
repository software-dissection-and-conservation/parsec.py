#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import generators

'''
Test the specification of parsec.py.
'''

__author__ = 'Daniel Edin, Micael Loberg and Tommy Vagbratt'

import random
import unittest

from parsec import *

class ParsecSpecificationTest(unittest.TestCase):
    '''Test the specification of parsec.py'''
    def test_times_with_then(_):
        parser = times(letter(), 3) >> digit()
        _.assertEqual(parser.parse('xyz1'), '1')
        _.assertRaises(ParseError, parser.parse, 'xy1')
        _.assertRaises(ParseError, parser.parse, 'xyz')
        _.assertRaises(ParseError, parser.parse, 'xyzw')

    def test_letter_parser(_):
        parser = letter()
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            _.assertEqual(parser.parse(c), c)
        for c in "0123456789+-.,;:?^*":
            _.assertRaises(ParseError, parser.parse, c)

        _.assertEqual(parser.parse('xyz1'), 'x')
        _.assertRaises(ParseError, parser.parse, '42')


if __name__ == '__main__':
    unittest.main()
