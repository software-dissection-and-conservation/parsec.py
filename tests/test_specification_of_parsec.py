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

class TommyTest(unittest.TestCase):
    """Test the specification of parsec.py"""
    def test_sepBy(_):
        parser = sepBy(string("x"), string(","))
        _.assertEqual(parser.parse("x"), ["x"])
        _.assertEqual(parser.parse("x,"), ["x"])
        _.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        _.assertEqual(parser.parse("") , [])
        _.assertEqual(parser.parse("1"), [])
        _.assertEqual(parser.parse("1,"), [])

    def test_sepBy1(_):
        parser = sepBy1(string("x"), string(","))
        _.assertEqual(parser.parse("x"), ["x"])
        _.assertEqual(parser.parse("x,"), ["x"])
        _.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        _.assertRaises(ParseError, parser.parse, "" )
        _.assertRaises(ParseError, parser.parse, "1")
        _.assertRaises(ParseError, parser.parse, "1,")

    def test_sepEndBy(_):
        parser = sepEndBy(string("x"), string(","))
        _.assertEqual(parser.parse("x"), ["x"])
        _.assertEqual(parser.parse("x,"), ["x"])
        _.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        _.assertEqual(parser.parse("") , [])
        _.assertEqual(parser.parse("1"), [])
        _.assertEqual(parser.parse("1,"), [])

    def test_sepEndBy1(_):
        parser = sepEndBy1(letter(), string(","))
        _.assertEqual(parser.parse("x"), ["x"])
        _.assertEqual(parser.parse("x,"), ["x"])
        _.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        _.assertRaises(ParseError, parser.parse, "" )
        _.assertRaises(ParseError, parser.parse, "1")
        _.assertRaises(ParseError, parser.parse, "1,")

    def test_separated(_):
        parser = separated(string("x"), string(","), 2, 5)
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertEqual(parser.parse("x,x"), ["x"]*2)
        _.assertEqual(parser.parse("x,x,"), ["x"]*2)
        _.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        _.assertEqual(parser.parse("x,x,x,x"), ["x"]*4)
        _.assertEqual(parser.parse("x,x,x,x,"), ["x"]*4)
        _.assertEqual(parser.parse("x,x,x,x,x"), ["x"]*5)
        _.assertEqual(parser.parse("x,x,x,x,x,"), ["x"]*5)
        _.assertEqual(parser.parse("x,x,x,x,x,x"), ["x"]*5) # one x remains to be consumed
        _.assertEqual(parser.parse("x,x,x,x,x,x,"), ["x"]*5) # one x remains to be consumed
        _.assertRaises(ParseError, parser.parse_strict, "x,x,x,x,x,x" )
        _.assertRaises(ParseError, parser.parse_strict, "x,x,x,x,x,x," )
        _.assertRaises(ParseError, parser.parse, "" )
        _.assertRaises(ParseError, parser.parse, "1")
        _.assertRaises(ParseError, parser.parse, "1,")

    def test_skip(_):
        parser = skip(string("x"), string("y"))
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "y")
        _.assertRaises(ParseError, parser.parse, "xx")
        _.assertRaises(ParseError, parser.parse, "yy")
        _.assertEqual(parser.parse("xy"), "x")
        _.assertRaises(ParseError, parser.parse_strict, "xyz")
        _.assertEqual(parser.parse("xyz"), "x") # z remains to be consumed

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
