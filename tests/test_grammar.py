#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the grammar parser
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import unittest

from pprint import pprint
from parsec.grammar import *

class GrammarTest(unittest.TestCase):
    """Test the grammar parser"""

    def test_many_of(self):
        p = many_of("xyz")
        valid = [ ""
                , "x"
                , "y"
                , "z"
                , "xyz"
                , "xxxxxxxxxxxyyyyyyyyyzzzzzz"
                , "yxyxyxyxyxyxzxyzxyyzxyzxyzyxyzxyzyxyzyyxyyxzyyzyxzyxyxxzz"
                ]
        for s in valid:
            self.assertEqual(p.parse_strict(s), list(s))

        invalid = [ "a"
                  , "b"
                  , "c"
                  , "sdfg"
                  , "2342"
                  , "fdkljdfjfdljaskjdfhaohofihoiehfihfsd"
                  , "With great power, comes...    awesomeness!"
                  ]
        for s in invalid:
            self.assertEqual(p.parse(s), [])

    def test_array_to_string(self):
        samples = [ "a"
                  , "b"
                  , "c"
                  , "sdfg"
                  , "2342"
                  , "fdkljdfjfdljaskjdfhaohofihoiehfihfsd"
                  , "With great power, comes...    awesomeness!"
                  ]
        for s in samples:
            self.assertEqual(array_to_string(list(s)), s)

    def test_whitespace(self):
        p = whitespace
        for i in range(10):
            self.assertEqual(p.parse(" "*i), " "*i)
            self.assertEqual(p.parse("\n"*i), "\n"*i)
        self.assertEqual(p.parse(" \n  \n\n    "), " \n  \n\n    ")

    def test_trim(self):
        p = trim(string("x"))
        for before in range(10):
            for after in range(10):
                self.assertEqual(p.parse_strict(" "*before + "x" + " "*after), "x")

    def test_symbol(self):
        p = symbol("x")
        for before in range(10):
            for after in range(10):
                self.assertEqual(p.parse_strict(" "*before + "x" + " "*after), "x")

    def test_comment(self):
        p = comment
        self.assertEqual(p.parse("# this is a comment"), Comment("this is a comment"))
        self.assertEqual(p.parse("# this is a comment    "), Comment("this is a comment"))
        self.assertEqual(p.parse("   # this is a comment"), Comment("this is a comment"))
        self.assertEqual(p.parse("   # this is a comment   "), Comment("this is a comment"))
        self.assertEqual(p.parse_strict("# this is a comment!"), Comment("this is a comment!"))
        self.assertEqual(p.parse_strict("\n# this is a comment!\n"), Comment("this is a comment!"))

    def test_identifier(self):
        p = identifier
        valid = [ "a"
                , "b"
                , "c"
                , "foo"
                , "_bar"
                , "_123onetwothree"
                , "this_is_a_really_long_identifier"
                , "awesomeness"
                ]
        invalid = [ "1337"
                  , "!!asdf"
                  , "asdf--asd-f-asd-f"
                  ]
        for s in valid:
            self.assertEqual(p.parse_strict(s), s)
        for s in invalid:
            self.assertRaises(ParseError, p.parse_strict, s)

    def test_start(self):
        p = start
        self.assertEqual(p.parse_strict("start = E;"), Start("E"))
        self.assertEqual(p.parse_strict("start = grammar;"), Start("grammar"))
        self.assertEqual(p.parse_strict("   start   =    main ; "), Start("main"))
        self.assertEqual(p.parse_strict("start = E;"), Start("E"))
        self.assertRaises(ParseError, p.parse_strict, "starts = foo;")
        self.assertRaises(ParseError, p.parse_strict, "start = 123;")
        self.assertRaises(ParseError, p.parse_strict, "start != 123;")

    def test_string_value(self):
        p = string_value
        valid = [ "a"
                , "b"
                , "c"
                , "foo"
                , "_bar"
                , "_123onetwothree"
                , "this_is_a_really_long_identifier"
                , "awesomeness"
                ]
        special = { "\\\\" : "\\"
                  , "\/" : "/"
                  , "\\\"" : "\""
                  , "\\b" : "\b"
                  , "\\f" : "\f"
                  , "\\n" : "\n"
                  , "\\r" : "\r"
                  , "\\t" : "\t"
                  , "\\\"" : "\""
                  , "\\\"" : "\""
                  , "\\uffff" : "\uffff"
                  , "\\uabcd" : "\uabcd"
                  , "\\uabcd" : "\uabcd"
                  }
        invalid = [ "1337"
                  , "!!asdf"
                  , "asdf--asd-f-asd-f"
                  ]
        for s in valid:
            self.assertEqual(p.parse_strict('"{0}"'.format(s)), StringValue(s))
        for k, v in special.items():
            self.assertEqual(p.parse_strict('"{0}"'.format(s)), StringValue(s))
        for s in invalid:
            self.assertRaises(ParseError, p.parse_strict, s)

    def test_token(self):
        p = token
        self.assertEqual(p.parse('token foo = "bar";'), Token("foo", StringValue("bar")))
        self.assertEqual(p.parse('token bar = "foo";'), Token("bar", StringValue("foo")))
        self.assertEqual(p.parse('token quote = "\\"";'), Token("quote", StringValue("\"")))
        self.assertEqual(p.parse_strict('token foo = "bar";'), Token("foo", StringValue("bar")))
        self.assertEqual(p.parse_strict('token foo = \n"bar";'), Token("foo", StringValue("bar")))
        self.assertEqual(p.parse_strict('  token \nfoo = \n"bar"  ;   '), Token("foo", StringValue("bar")))
        self.assertRaises(ParseError, p.parse, 'tokens foo = "bar";')
        self.assertRaises(ParseError, p.parse, 'töken foo = "bar";')
        self.assertRaises(ParseError, p.parse, 'token foo != "bar";')
        self.assertRaises(ParseError, p.parse, 'token foo = bar;')
        self.assertRaises(ParseError, p.parse, 'token foo = "bar"')



if __name__ == "__main__":
    unittest.main()
