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
        start = Start(NameValue("root"))
        self.assertEqual(start.start_rule, NameValue("root"))
        self.assertEqual(str(start), "start = root;")

    def test_token(self):
        token = Token("while", StringValue("while"))
        self.assertEqual(token.name, "while")
        self.assertEqual(token.value, StringValue("while"))
        self.assertEqual(str(token), "token while = \"while\";")

    def test_string_value(self):
        v = StringValue("for")
        self.assertEqual(v.value, "for")
        self.assertEqual(str(v), "\"for\"")

    def test_name_value(self):
        v = NameValue("grammar")
        self.assertEqual(v.name, "grammar")
        self.assertEqual(str(v), "grammar")

    def test_production(self):
        production = Production([StringValue("def"), NameValue("identifier"), StringValue("\\n"), NameValue("body")])
        self.assertEqual(production.parts, [StringValue("def"), NameValue("identifier"), StringValue("\\n"), NameValue("body")])
        self.assertEqual(str(production), "\"def\" identifier \"\\n\" body")

    def test_rule(self):
        rule = Rule("declaration", [Production([StringValue("var"), NameValue("identifier"), StringValue(";")]), Production([StringValue("val"), NameValue("identifier"), StringValue(";")])])
        self.assertEqual(rule.name, "declaration")
        self.assertEqual(rule.productions, [Production([StringValue("var"), NameValue("identifier"), StringValue(";")]), Production([StringValue("val"), NameValue("identifier"), StringValue(";")])])
        self.assertEqual(str(rule), "declaration = \"var\" identifier \";\" | \"val\" identifier \";\";")

if __name__ == "__main__":
    unittest.main()
