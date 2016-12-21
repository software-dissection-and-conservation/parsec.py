#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the semantic analysis
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import unittest

from parsec import *
from parsec.semantic import *

class SemanticTest(unittest.TestCase):
    """Test the semantic"""
    def test_correct_grammar(self):
        g1 = Grammar([Comment("this is a comment")])
        g2 = Grammar([Token("foo", String("bar"))])
        g3 = Grammar([ Token("fun", String("bar"))
                     , Rule("foo", [Production([Identifier("fun")])])
                     ])
        g4 = Grammar([ Comment("This is a grammar")
                     , Comment("Here we define some tokens")
                     , Token("a", String("x"))
                     , Token("b1", String("x1"))
                     , Token("b2", String("x2"))
                     , Token("_", String("_"))
                     , Comment("And here come the grammar rules")
                     , Rule("foo", [ Production([Identifier("a"), Identifier("other")]) , Production([Identifier("_")]) ])
                     , Rule("other", [ Production([Identifier("b1")]) , Production([Identifier("b2")]) , Production([String("hey!")]) ])
                     , Comment("Please start at foo")
                     , Start("foo")
                     ])
        self.assertTrue(validate_ast(g1))
        self.assertTrue(validate_ast(g2))
        self.assertTrue(validate_ast(g3))
        self.assertTrue(validate_ast(g4))


    def test_incorrect_grammar(self):
        g1 = Grammar([ Token("foo", String("bar"))
                     , Token("foo", String("baz"))
                     ])
        g2 = Grammar([ Token("foo", String("bar"))
                     , Rule("foo", [])
                     ])
        g3 = Grammar([ Rule("foo", [])
                     , Rule("foo", [])
                     ])
        g4 = Grammar([ Comment("This is a grammar")
                     , Comment("Here we define some tokens")
                     , Token("a", String("x"))
                     , Token("b2", String("x1"))
                     , Token("b2", String("x2"))
                     , Token("_", String("_"))
                     , Comment("And here come the grammar rules")
                     , Rule("foo", [ Production([Identifier("a"), Identifier("other")]) , Production([Identifier("_")]) ])
                     , Rule("other", [ Production([Identifier("b1")]) , Production([Identifier("b2")]) , Production([String("hey!")]) ])
                     , Comment("Please start at foo")
                     , Start("foo")
                     ])
        self.assertRaises(SemanticError, validate_ast, g1)
        self.assertRaises(SemanticError, validate_ast, g2)
        self.assertRaises(SemanticError, validate_ast, g3)
        self.assertRaises(SemanticError, validate_ast, g4)

    def test_undefined_identifiers(self):
        g1 = Grammar([ Token("defined", String("bar"))
                      , Rule("foo", [Production([Identifier("undefined")])])
                      ])
        g2 = Grammar([ Comment("This is a grammar")
                     , Comment("Here we define some tokens")
                     , Token("a", String("x"))
                     , Token("b1", String("x1"))
                     , Token("b2", String("x2"))
                     , Comment("And here come the grammar rules")
                     , Rule("foo", [ Production([Identifier("a"), Identifier("other")]) , Production([Identifier("_")]) ])
                     , Rule("other", [ Production([Identifier("b1")]) , Production([Identifier("b2")]) , Production([String("hey!")]) ])
                     , Comment("Please start at foo")
                     , Start("foo")
                     ])
        self.assertRaises(SemanticError, validate_ast, g1)
        self.assertRaises(SemanticError, validate_ast, g2)




if __name__ == "__main__":
    unittest.main()
