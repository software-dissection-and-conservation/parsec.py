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



if __name__ == "__main__":
    unittest.main()
