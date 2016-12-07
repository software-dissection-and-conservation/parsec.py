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

    def test_skip_operator(_):
        parser = string("x") << string("y")
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "y")
        _.assertRaises(ParseError, parser.parse, "xx")
        _.assertRaises(ParseError, parser.parse, "yy")
        _.assertEqual(parser.parse("xy"), "x")
        _.assertRaises(ParseError, parser.parse_strict, "xyz")
        _.assertEqual(parser.parse("xyz"), "x") # z remains to be consumed

    def test_space(_):
        parser = space()
        _.assertEqual(parser.parse(" "), " ")
        _.assertEqual(parser.parse("  "), " ") # one space left to be consumed
        _.assertRaises(ParseError, parser.parse, "")
        _.assertRaises(ParseError, parser.parse, "x ")

    def test_spaces(_):
        parser = spaces()
        _.assertEqual(parser.parse(""), [])
        _.assertEqual(parser.parse(" "), [" "])
        _.assertEqual(parser.parse("  "), [" "]*2)
        _.assertEqual(parser.parse("c . . ."), [])

    def test_string(_):
        parser = string("x")
        _.assertRaises(ParseError, parser.parse, "")
        _.assertEqual(parser.parse("x"), "x")
        _.assertEqual(parser.parse("xy"), "x") # y remains to be consumed
        _.assertRaises(ParseError, parser.parse, " xxx")

    def test_times(_):
        parser = times(string("x"), 3, 5)
        _.assertRaises(ParseError, parser.parse, "")
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "xx")
        _.assertEqual(parser.parse("xxx"), ["x"]*3)
        _.assertEqual(parser.parse("xxxx"), ["x"]*4)
        _.assertEqual(parser.parse("xxxxx"), ["x"]*5)
        _.assertEqual(parser.parse("xxxxxx"), ["x"]*5) # one x remains to be consumed
        _.assertRaises(ParseError, parser.parse_strict, "xxxxxx")
        _.assertRaises(ParseError, parser.parse_strict, "xxxxxxx")

    def test_try_choice(_):
        parser = try_choice(string("-x"), string("-y"))
        _.assertRaises(ParseError, parser.parse, "")
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "y")
        _.assertEqual(parser.parse("-x"), "-x")
        _.assertEqual(parser.parse("-y"), "-y")
        _.assertEqual(parser.parse("-xy"), "-x") # y remains to be consumed
        _.assertRaises(ParseError, parser.parse, "-z")
        _.assertRaises(ParseError, parser.parse, "abc")

    def test_try_choice_operator(_):
        parser = string("-x") ^ string("-y")
        _.assertRaises(ParseError, parser.parse, "")
        _.assertRaises(ParseError, parser.parse, "x")
        _.assertRaises(ParseError, parser.parse, "y")
        _.assertEqual(parser.parse("-x"), "-x")
        _.assertEqual(parser.parse("-y"), "-y")
        _.assertEqual(parser.parse("-xy"), "-x") # y remains to be consumed
        _.assertRaises(ParseError, parser.parse, "-z")
        _.assertRaises(ParseError, parser.parse, "abc")

    def test_generate(_):
        nonlocals = {"[": None, "]": None}
        @generate
        def array_of_xs():
            nonlocals["["] = yield string("[")
            array_elements = yield sepBy(string("x"), spaces() >> string(",") << spaces())
            nonlocals["]"] = yield string("]")
            return array_elements

        _.assertEqual(nonlocals["["], None)
        _.assertEqual(nonlocals["]"], None)
        _.assertEqual(array_of_xs.parse("[x, x, x,x, x]"), ["x"]*5)
        _.assertEqual(nonlocals["["], "[")
        _.assertEqual(nonlocals["]"], "]")



class DanielTest(unittest.TestCase):
    '''Test the implementation of Text.Parsec.Char.'''

    def test_letter(self):
        parser = letter()
        self.assertEqual(parser.parse('A'), 'A')
        self.assertRaises(ParseError, parser.parse, '9')

    def test_many(self):
        parser = many(letter())
        self.assertEqual(parser.parse(''), [])
        self.assertEqual(parser.parse('x'), ['x'])
        self.assertEqual(parser.parse('abcO'), ['a', 'b', 'c', 'O'])

    def test_many1(self):
        parser = many1(letter())
        self.assertEqual(parser.parse('x'), ['x'])
        self.assertEqual(parser.parse('abcO'), ['a', 'b', 'c', 'O'])
        self.assertRaises(ParseError, parser.parse, '*')

    def test_mark(self):
        parser = many(mark(many(letter())) << (string(";") | string("\n")))

        lines = parser.parse("asdf;kappa;then\nelse\n")

        self.assertEqual(len(lines), 4)

        (start, letters, end) = lines[0]
        self.assertEqual(start, (0, 0))
        self.assertEqual(letters, ['a', 's', 'd', 'f'])
        self.assertEqual(end, (0, 4))

        (start, letters, end) = lines[1]
        self.assertEqual(start, (0, 5))
        self.assertEqual(letters, ['k', 'a', 'p', 'p', 'a'])
        self.assertEqual(end, (0, 10))

        (start, letters, end) = lines[2]
        self.assertEqual(start, (0, 11))
        self.assertEqual(letters, ['t', 'h', 'e', 'n'])
        self.assertEqual(end, (0, 15))

        (start, letters, end) = lines[3]
        self.assertEqual(start, (1, 0))
        self.assertEqual(letters, ['e', 'l', 's', 'e'])
        self.assertEqual(end, (1, 4))

    def test_none_of(self):
        parser = none_of("()[]{}")
        self.assertEqual(parser.parse('test'), 't')
        self.assertEqual(many(parser).parse('test'), ['t', 'e', 's', 't'])
        self.assertRaises(ParseError, parser.parse, '[]')

    def test_one_of(self):
        parser = one_of("()[]{}")
        self.assertEqual(parser.parse('()'), '(')
        self.assertEqual(many(parser).parse('()'), ['(', ')'])
        self.assertRaises(ParseError, parser.parse, 'y')

    def test_parse(self):
        self.assertEqual(letter().parse("x"), 'x')
        self.assertEqual(letter().parse("yX"), 'y')
        self.assertRaises(ParseError, letter().parse, '2')

    # TODO
   # def test_parse_operator(self):
   #     self.assertEqual(parse(letter(), "x", 0), 'x')


    def test_parse_partial(self):
        self.assertEqual(letter().parse_partial("x_rest"), ('x', '_rest'))
        self.assertRaises(ParseError, letter().parse_partial, "1")

    def test_parse_strict(self):
        self.assertEqual(letter().parse_strict("x"), 'x')
        self.assertEqual(string("").parse_strict(""), '')
        self.assertRaises(ParseError, letter().parse_strict, "1")

    def test_parsecmap(self):
        parser = letter().parsecmap(str.upper)
        self.assertEqual(parser.parse("x"), 'X')

    def test_parsecmap_operator(self):
        self.assertEqual(parsecmap(letter(), str.upper).parse("x"), 'X')

    def test_result(self):

        parser = letter().result("New result")
        self.assertEqual(parser.parse("x"), "New result")

        self.assertRaises(ParseError, parser.parse, "1")

    def test_result_operator(self):
        self.assertEqual(result(letter(), "New result").parse("x"), 'New result')

    def test_regex(self):
        parser = regex(r'[a-z]')
        self.assertEqual(parser.parse('abc'), 'a')
        self.assertEqual(parser.parse('x'), 'x')
        self.assertRaises(ParseError, parser.parse, '2')






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
