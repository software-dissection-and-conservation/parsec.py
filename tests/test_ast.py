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
        token = Token("while", "while")
        self.assertEqual(token.name, "while")
        self.assertEqual(token.value, "while")
        self.assertEqual(str(token), "token while = \"while\";")

if __name__ == "__main__":
    unittest.main()
