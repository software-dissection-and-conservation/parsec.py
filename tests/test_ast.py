#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Test the Abstract Syntax Tree
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import unittest

from parsec import *
from parsec.ast import *

class AbstractSyntaxTreeTest(unittest.TestCase):
    """Test the Abstract Syntax Tree"""

    def test_comment(self):
        comment = Comment("this is a comment")
        self.assertEqual(comment.message, "this is a comment")
        self.assertEqual(str(comment), "# this is a comment")

    def test_start(self):
        start = Start("root")
        self.assertEqual(start.start_rule, "root")
        self.assertEqual(str(start), "start = root;")

    def test_token(self):
        token = Token("while", String("while"))
        self.assertEqual(token.name, "while")
        self.assertEqual(token.value, String("while"))
        self.assertEqual(str(token), "token while = \"while\";")

    def test_string_value(self):
        s = String("for")
        self.assertEqual(s.value, "for")
        self.assertEqual(str(s), "\"for\"")

    def test_regular_expression(self):
        r = RegularExpression("\\d+")
        self.assertEqual(r.value, "\\d+")
        self.assertEqual(str(r), "r\"\\d+\"")

    def test_identifier(self):
        v = Identifier("grammar")
        self.assertEqual(v.name, "grammar")
        self.assertEqual(str(v), "grammar")

    def test_production(self):
        production = Production([String("def"), Identifier("identifier"), String("\\n"), Identifier("body")])
        self.assertEqual(production.parts, [String("def"), Identifier("identifier"), String("\\n"), Identifier("body")])
        self.assertEqual(str(production), "\"def\" identifier \"\\n\" body")

    def test_rule(self):
        rule = Rule("declaration", [Production([String("var"), Identifier("identifier"), String(";")]), Production([String("val"), Identifier("identifier"), String(";")])])
        self.assertEqual(rule.name, "declaration")
        self.assertEqual(rule.productions, [Production([String("var"), Identifier("identifier"), String(";")]), Production([String("val"), Identifier("identifier"), String(";")])])
        self.assertEqual(str(rule), "declaration = \"var\" identifier \";\" | \"val\" identifier \";\";")

if __name__ == "__main__":
    unittest.main()
