#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Test the Abstract Syntax Tree
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import unittest
import tempfile

from parsec import *
from parsec.ast import *
from parsec.ast import *
from parsec.create_python_file import *

class CodeGenerationTest(unittest.TestCase):


    def test_generated_parser(self):

        grammar = '''# this is a comments
token plus = "+";
start = E;
# Grammar;
num = "1";
E = T X;
T = "(" E ")" | num Y;
X = plus E | "";
Y = "*" T | "";
'''
        grammar_temp = tempfile.NamedTemporaryFile()
        #code_gen_temp = tempfile.NamedTemporaryFile()

        with open(grammar_temp.name, 'w') as f:
            f.write(grammar)



        parse_grammar(grammar_temp.name)
        create_func("code_gen_temp.py", "my_parser", "generated", 1)

        import code_gen_temp

        parser = code_gen_temp.my_parser

        self.assertEqual(parser.parse("1+1"), (('1', ''), ('+', (('1', ''), ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")

        parser = code_gen_temp.generated()
        self.assertEqual(parser.parse("1+1"), (('1', ''), ('+', (('1', ''), ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")

        grammar_temp.close()


    def test_multiple_tokens(self):

        grammar = '''token plus = "+";
token plus = "*";
'''
        grammar_temp = tempfile.NamedTemporaryFile()

        with open(grammar_temp.name, 'w') as f:
            f.write(grammar)

        #TODO change the exception to the one validate_ast will throw
        self.assertRaises(NameError, parse_grammar, grammar_temp.name)
        grammar_temp.close()

if __name__ == "__main__":
    unittest.main()
