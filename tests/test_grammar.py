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

    def test_identifier_value(self):
        p = identifier_value
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
            self.assertEqual(p.parse_strict(s), Identifier(s))
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
            self.assertEqual(p.parse_strict('"{0}"'.format(s)), String(s))
        for k, v in special.items():
            self.assertEqual(p.parse_strict('"{0}"'.format(s)), String(s))
        for s in invalid:
            self.assertRaises(ParseError, p.parse_strict, s)

    def test_token(self):
        p = token
        self.assertEqual(p.parse_strict('token foo = "bar";'), Token("foo", String("bar")))
        self.assertEqual(p.parse_strict('token bar = "foo";'), Token("bar", String("foo")))
        self.assertEqual(p.parse_strict('token quote = "\\"";'), Token("quote", String("\"")))
        self.assertEqual(p.parse_strict('token foo = "bar";'), Token("foo", String("bar")))
        self.assertEqual(p.parse_strict('token foo = \n"bar";'), Token("foo", String("bar")))
        self.assertEqual(p.parse_strict('  token \nfoo = \n"bar"  ;   '), Token("foo", String("bar")))
        self.assertRaises(ParseError, p.parse, 'tokens foo = "bar";')
        self.assertRaises(ParseError, p.parse, 'töken foo = "bar";')
        self.assertRaises(ParseError, p.parse, 'token foo != "bar";')
        self.assertRaises(ParseError, p.parse, 'token foo = bar;')
        self.assertRaises(ParseError, p.parse, 'token foo = "bar"')

    def test_production(self):
        p = production
        self.assertEqual(p.parse_strict('"foo"'), Production([String("foo")]))
        self.assertEqual(p.parse_strict('    "foo"   '), Production([String("foo")]))
        self.assertEqual(p.parse_strict('"foo" "bar"'), Production([String("foo"), String("bar")]))
        self.assertEqual(p.parse_strict('  "foo" \n "bar" \n \n'), Production([String("foo"), String("bar")]))
        self.assertEqual(p.parse_strict('"foo" "bar" "baz"'), Production([String("foo"), String("bar"), String("baz")]))
        self.assertEqual(p.parse_strict('foo'), Production([Identifier("foo")]))
        self.assertEqual(p.parse_strict('foo bar'), Production([Identifier("foo"), Identifier("bar")]))
        self.assertEqual(p.parse_strict('foo "foo"'), Production([Identifier("foo"), String("foo")]))
        self.assertEqual(p.parse_strict('foo "bar" baz'), Production([Identifier("foo"), String("bar"), Identifier("baz")]))
        self.assertEqual(p.parse('foo | bar'), Production([Identifier("foo")])) # Note: "| bar" remains to be consumed
        self.assertRaises(ParseError,p.parse_strict, 'foo | bar')
        self.assertRaises(ParseError,p.parse_strict, '!foo | bar')
        self.assertRaises(ParseError,p.parse_strict, 'foo bar!')
        self.assertRaises(ParseError,p.parse_strict, 'foo?')

    def test_rule(self):
        p = rule
        self.assertEqual(p.parse_strict('foo = "bar";'), Rule("foo", [Production([String("bar")])]))
        self.assertEqual(p.parse_strict('foo = bar;'), Rule("foo", [Production([Identifier("bar")])]))
        self.assertEqual(p.parse_strict('_ = _;'), Rule("_", [Production([Identifier("_")])]))
        self.assertEqual(p.parse_strict('foo = "bar" "baz";'), Rule("foo", [Production([String("bar"), String("baz")])]))
        self.assertEqual(p.parse_strict('foo = "bar" baz | x y z | "foo";'), Rule("foo", [Production([String("bar"), Identifier("baz")]), Production([Identifier("x"), Identifier("y"), Identifier("z")]), Production([String("foo")])]))
        self.assertEqual(p.parse_strict('foo = "bar" | "baz";'), Rule("foo", [Production([String("bar")]), Production([String("baz")])]))
        self.assertEqual(p.parse_strict('foo = "bar" "baz";'), Rule("foo", [Production([String("bar"), String("baz")])]))
        self.assertEqual(p.parse_strict('foo1 = "bar"\n | "baz";'), Rule("foo1", [Production([String("bar")]), Production([String("baz")])]))
        self.assertEqual(p.parse_strict('foo = "bar"\n | \n "baz";'), Rule("foo", [Production([String("bar")]), Production([String("baz")])]))
        self.assertEqual(p.parse_strict(' \n foo \n = \n "bar"\n | \n "baz" \n  ; \n'), Rule("foo", [Production([String("bar")]), Production([String("baz")])]))

    def test_grammar(self):
        p = grammar
        self.assertEqual(p.parse_strict("start = foo;"), Grammar([Start("foo")]))
        self.assertEqual(p.parse_strict('start = foo;\ntoken a = "b";'), Grammar([Start("foo"), Token("a", String("b"))]))
        self.assertEqual(p.parse_strict('start = foo;\ntoken bar = "baz";\n foo = bar;'), Grammar([ Start("foo")
                                                                                          , Token("bar", String("baz"))
                                                                                          , Rule("foo", [Production([Identifier("bar")])])
                                                                                          ]))
        self.assertEqual(p.parse_strict('# this is a comment \nstart = foo;\ntoken bar = "baz";\n foo = bar;'), Grammar([ Comment("this is a comment")
                                                                                                                        , Start("foo")
                                                                                                                        , Token("bar", String("baz"))
                                                                                                                        , Rule("foo", [Production([Identifier("bar")])])
                                                                                                                        ]))
        test_grammar = """
# This is a grammar

# Here we define some tokens
token a = "x";
token b1 = "x1";
token b2 = "x2";

# And here come the grammar rules
foo = a other
    | _
    ;

other = b1
      | b2
      | "hey!"
      ;

# Please start at foo

start = foo;

"""
        print(p.parse(test_grammar))
        self.assertEqual(p.parse(test_grammar), Grammar([ Comment("This is a grammar")
                                                        , Comment("Here we define some tokens")
                                                        , Token("a", String("x"))
                                                        , Token("b1", String("x1"))
                                                        , Token("b2", String("x2"))
                                                        , Comment("And here come the grammar rules")
                                                        , Rule("foo", [ Production([Identifier("a"), Identifier("other")])
                                                                      , Production([Identifier("_")])
                                                                      ])
                                                        , Rule("other", [ Production([Identifier("b1")])
                                                                        , Production([Identifier("b2")])
                                                                        , Production([String("hey!")])
                                                                        ])
                                                        , Comment("Please start at foo")
                                                        , Start("foo")
                                                        ]))



if __name__ == "__main__":
    unittest.main()
