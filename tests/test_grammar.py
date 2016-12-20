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



if __name__ == "__main__":
    unittest.main()
