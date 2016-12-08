#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import generators

"""
Test the specification of parsec.py.
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import unittest

from parsec import *

class ParsecSpecificationTest(unittest.TestCase):
    """Test the specification of parsec.py"""
    def test_sepBy(self):
        parser = sepBy(string("x"), string(","))
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("x,"), ["x"])
        self.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        self.assertEqual(parser.parse("") , [])
        self.assertEqual(parser.parse("1"), [])
        self.assertEqual(parser.parse("1,"), [])

    def test_sepBy1(self):
        parser = sepBy1(string("x"), string(","))
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("x,"), ["x"])
        self.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        self.assertRaises(ParseError, parser.parse, "" )
        self.assertRaises(ParseError, parser.parse, "1")
        self.assertRaises(ParseError, parser.parse, "1,")

    def test_sepEndBy(self):
        parser = sepEndBy(string("x"), string(","))
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("x,"), ["x"])
        self.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        self.assertEqual(parser.parse("") , [])
        self.assertEqual(parser.parse("1"), [])
        self.assertEqual(parser.parse("1,"), [])

    def test_sepEndBy1(self):
        parser = sepEndBy1(letter(), string(","))
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("x,"), ["x"])
        self.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        self.assertRaises(ParseError, parser.parse, "" )
        self.assertRaises(ParseError, parser.parse, "1")
        self.assertRaises(ParseError, parser.parse, "1,")

    def test_separated(self):
        parser = separated(string("x"), string(","), 2, 5)
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertEqual(parser.parse("x,x"), ["x"]*2)
        self.assertEqual(parser.parse("x,x,"), ["x"]*2)
        self.assertEqual(parser.parse("x,x,x"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,"), ["x"]*3)
        self.assertEqual(parser.parse("x,x,x,x"), ["x"]*4)
        self.assertEqual(parser.parse("x,x,x,x,"), ["x"]*4)
        self.assertEqual(parser.parse("x,x,x,x,x"), ["x"]*5)
        self.assertEqual(parser.parse("x,x,x,x,x,"), ["x"]*5)
        self.assertEqual(parser.parse("x,x,x,x,x,x"), ["x"]*5) # one x remains to be consumed
        self.assertEqual(parser.parse("x,x,x,x,x,x,"), ["x"]*5) # one x remains to be consumed
        self.assertRaises(ParseError, parser.parse_strict, "x,x,x,x,x,x" )
        self.assertRaises(ParseError, parser.parse_strict, "x,x,x,x,x,x," )
        self.assertRaises(ParseError, parser.parse, "" )
        self.assertRaises(ParseError, parser.parse, "1")
        self.assertRaises(ParseError, parser.parse, "1,")

    def test_skip(self):
        parser = skip(string("x"), string("y"))
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "y")
        self.assertRaises(ParseError, parser.parse, "xx")
        self.assertRaises(ParseError, parser.parse, "yy")
        self.assertEqual(parser.parse("xy"), "x")
        self.assertRaises(ParseError, parser.parse_strict, "xyz")
        self.assertEqual(parser.parse("xyz"), "x") # z remains to be consumed

    def test_skip_operator(self):
        parser = string("x") << string("y")
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "y")
        self.assertRaises(ParseError, parser.parse, "xx")
        self.assertRaises(ParseError, parser.parse, "yy")
        self.assertEqual(parser.parse("xy"), "x")
        self.assertRaises(ParseError, parser.parse_strict, "xyz")
        self.assertEqual(parser.parse("xyz"), "x") # z remains to be consumed

    def test_space(self):
        parser = space()
        self.assertEqual(parser.parse(" "), " ")
        self.assertEqual(parser.parse("  "), " ") # one space left to be consumed
        self.assertRaises(ParseError, parser.parse, "")
        self.assertRaises(ParseError, parser.parse, "x ")

    def test_spaces(self):
        parser = spaces()
        self.assertEqual(parser.parse(""), [])
        self.assertEqual(parser.parse(" "), [" "])
        self.assertEqual(parser.parse("  "), [" "]*2)
        self.assertEqual(parser.parse("c . . ."), [])

    def test_string(self):
        parser = string("x")
        self.assertRaises(ParseError, parser.parse, "")
        self.assertEqual(parser.parse("x"), "x")
        self.assertEqual(parser.parse("xy"), "x") # y remains to be consumed
        self.assertRaises(ParseError, parser.parse, " xxx")

    def test_times(self):
        parser = times(string("x"), 3, 5)
        self.assertRaises(ParseError, parser.parse, "")
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "xx")
        self.assertEqual(parser.parse("xxx"), ["x"]*3)
        self.assertEqual(parser.parse("xxxx"), ["x"]*4)
        self.assertEqual(parser.parse("xxxxx"), ["x"]*5)
        self.assertEqual(parser.parse("xxxxxx"), ["x"]*5) # one x remains to be consumed
        self.assertRaises(ParseError, parser.parse_strict, "xxxxxx")
        self.assertRaises(ParseError, parser.parse_strict, "xxxxxxx")

    def test_try_choice(self):
        parser = try_choice(string("-x"), string("-y"))
        self.assertRaises(ParseError, parser.parse, "")
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "y")
        self.assertEqual(parser.parse("-x"), "-x")
        self.assertEqual(parser.parse("-y"), "-y")
        self.assertEqual(parser.parse("-xy"), "-x") # y remains to be consumed
        self.assertRaises(ParseError, parser.parse, "-z")
        self.assertRaises(ParseError, parser.parse, "abc")

    def test_try_choice_operator(self):
        parser = string("-x") ^ string("-y")
        self.assertRaises(ParseError, parser.parse, "")
        self.assertRaises(ParseError, parser.parse, "x")
        self.assertRaises(ParseError, parser.parse, "y")
        self.assertEqual(parser.parse("-x"), "-x")
        self.assertEqual(parser.parse("-y"), "-y")
        self.assertEqual(parser.parse("-xy"), "-x") # y remains to be consumed
        self.assertRaises(ParseError, parser.parse, "-z")
        self.assertRaises(ParseError, parser.parse, "abc")

    def test_generate(self):
        nonlocals = {"[": None, "]": None}
        @generate
        def array_of_xs():
            nonlocals["["] = yield string("[")
            array_elements = yield sepBy(string("x"), spaces() >> string(",") << spaces())
            nonlocals["]"] = yield string("]")
            return array_elements

        self.assertEqual(nonlocals["["], None)
        self.assertEqual(nonlocals["]"], None)
        self.assertEqual(array_of_xs.parse("[x, x, x,x, x]"), ["x"]*5)
        self.assertEqual(nonlocals["["], "[")
        self.assertEqual(nonlocals["]"], "]")

    def test_letter_parser(self):
        parser = letter()
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            self.assertEqual(parser.parse(c), c)
        for c in "0123456789+-.,;:?^*":
            self.assertRaises(ParseError, parser.parse, c)

        self.assertEqual(parser.parse("xyz1"), "x")
        self.assertRaises(ParseError, parser.parse, "42")

    def test_letter(self):
        parser = letter()
        self.assertEqual(parser.parse("A"), "A")
        self.assertRaises(ParseError, parser.parse, "9")

    def test_many(self):
        parser = many(letter())
        self.assertEqual(parser.parse(""), [])
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("abcO"), ["a", "b", "c", "O"])

    def test_many1(self):
        parser = many1(letter())
        self.assertEqual(parser.parse("x"), ["x"])
        self.assertEqual(parser.parse("abcO"), ["a", "b", "c", "O"])
        self.assertRaises(ParseError, parser.parse, "*")

    def test_mark(self):
        parser = many(mark(many(letter())) << (string(";") | string("\n")))

        lines = parser.parse("asdf;kappa;then\nelse\n")

        self.assertEqual(len(lines), 4)

        (start, letters, end) = lines[0]
        self.assertEqual(start, (0, 0))
        self.assertEqual(letters, ["a", "s", "d", "f"])
        self.assertEqual(end, (0, 4))

        (start, letters, end) = lines[1]
        self.assertEqual(start, (0, 5))
        self.assertEqual(letters, ["k", "a", "p", "p", "a"])
        self.assertEqual(end, (0, 10))

        (start, letters, end) = lines[2]
        self.assertEqual(start, (0, 11))
        self.assertEqual(letters, ["t", "h", "e", "n"])
        self.assertEqual(end, (0, 15))

        (start, letters, end) = lines[3]
        self.assertEqual(start, (1, 0))
        self.assertEqual(letters, ["e", "l", "s", "e"])
        self.assertEqual(end, (1, 4))

    def test_none_of(self):
        parser = none_of("()[]{}")
        self.assertEqual(parser.parse("test"), "t")
        self.assertEqual(many(parser).parse("test"), ["t", "e", "s", "t"])
        self.assertRaises(ParseError, parser.parse, "[]")

    def test_one_of(self):
        parser = one_of("()[]{}")
        self.assertEqual(parser.parse("()"), "(")
        self.assertEqual(many(parser).parse("()"), ["(", ")"])
        self.assertRaises(ParseError, parser.parse, "y")

    def test_parse(self):
        self.assertEqual(letter().parse("x"), "x")
        self.assertEqual(letter().parse("yX"), "y")
        self.assertRaises(ParseError, letter().parse, "2")

    def test_parse_fn(self):
        self.assertEqual(parse(letter(), "x"), "x")
        self.assertEqual(parse(digit(), "1"), "1")
        self.assertRaises(ParseError, lambda : parse(letter(), "42"))
        self.assertRaises(ParseError, lambda : parse(letter(), "42"))

    def test_parse_partial(self):
        self.assertEqual(letter().parse_partial("x_rest"), ("x", "_rest"))
        self.assertRaises(ParseError, letter().parse_partial, "1")

    def test_parse_strict(self):
        self.assertEqual(letter().parse_strict("x"), "x")
        self.assertEqual(string("").parse_strict(""), "")
        self.assertRaises(ParseError, letter().parse_strict, "1")

    def test_parsecmap(self):
        parser = letter().parsecmap(str.upper)
        self.assertEqual(parser.parse("x"), "X")

    def test_parsecmap_operator(self):
        self.assertEqual(parsecmap(letter(), str.upper).parse("x"), "X")

    def test_result(self):

        parser = letter().result("New result")
        self.assertEqual(parser.parse("x"), "New result")

        self.assertRaises(ParseError, parser.parse, "1")

    def test_result_operator(self):
        self.assertEqual(result(letter(), "New result").parse("x"), "New result")

    def test_regex(self):
        parser = regex(r"[a-z]")
        self.assertEqual(parser.parse("abc"), "a")
        self.assertEqual(parser.parse("x"), "x")
        self.assertRaises(ParseError, parser.parse, "2")

    def test_digit(self):
        parser = digit()
        self.assertEqual(parser.parse("1"), "1")
        self.assertRaises(ParseError, parser.parse, "a")

    def test_bind(self):
        cookies = [""]
        def end_with_b(beforeB):
            cookies[0] = "".join(beforeB)
            return string("b")

        parser = many(digit()).bind(end_with_b)
        self.assertEqual(parser.parse('111b'), 'b')
        self.assertEqual(cookies[0], "111")

    def test_choice(self):
        parser1 = digit()
        parser2 = letter()
        choice = parser1 | parser2
        self.assertEqual(choice.parse("A1"), "A")
        self.assertEqual(choice.parse("1A"), "1")
        self.assertRaises(ParseError, choice.parse, "!7")

    def test_count(self):
        parser = count(digit(), 7)
        self.assertEqual(parser.parse("7777777"), ["7", "7", "7", "7", "7", "7", "7"])
        self.assertEqual(parser.parse("7777777A"), ["7", "7", "7", "7", "7", "7", "7"])
        self.assertEqual(parser.parse("123456789"), ["1", "2", "3", "4", "5", "6", "7"])
        self.assertRaises(ParseError, parser.parse, "123456")

    def test_compose(self):
        parser = digit() >> letter()
        self.assertEqual(parser.parse("1A"), "A")
        self.assertEqual(parser.parse("2AB"), "A")
        self.assertRaises(ParseError, parser.parse, "12A")
        self.assertRaises(ParseError, parser.parse, "A1")

    def test_endBy(self):
        parser = endBy(letter(), digit())
        self.assertEqual(parser.parse("A1"), ["A"])
        self.assertEqual(parser.parse("A1B2"), ["A", "B"])
        self.assertEqual(parser.parse("1A2"), [])
        self.assertEqual(parser.parse("A1B23"), ["A", "B"])
        self.assertRaises(ParseError, parser.parse, "A2B")

    def test_endBy1(self):
        parser = endBy(letter(), digit())
        self.assertEqual(parser.parse("A1"), ["A"])
        self.assertEqual(parser.parse("A1B2"), ["A", "B"])
        self.assertEqual(parser.parse("1A2"), [])
        self.assertEqual(parser.parse("A1B23"), ["A", "B"])
        self.assertRaises(ParseError, parser.parse, "A2B")

    def test_ends_with(self):
        parser = letter() < digit()
        self.assertEqual(parser.parse("a2"), "a")
        self.assertRaises(ParseError, parser.parse, "a")

    def test_joint(self):
        parser = letter() + digit()
        self.assertEqual(parser.parse("A2"), ("A", "2"))
        self.assertRaises(ParseError, parser.parse, "a")


if __name__ == "__main__":
    unittest.main()
