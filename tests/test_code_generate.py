#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Test the Abstract Syntax Tree
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import unittest
import tempfile
import importlib

from parsec import *
from parsec.ast import *
from parsec.semantic import *
from parsec.create_python_file import *

class CodeGenerationTest(unittest.TestCase):


    def test_generate_not_hidden(self):

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

        with open(grammar_temp.name, 'w') as f:
            f.write(grammar)



        obj = parse_grammar(grammar_temp.name, True)
        create_func(obj, "code_gen_temp.py", "my_parser", "generated", False)

        import code_gen_temp

        parser = code_gen_temp.my_parser

        self.assertEqual(parser.parse("1+1"), (('1', ''), ('+', (('1', ''), ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")

        parser = code_gen_temp.num

        self.assertEqual(parser.parse("1"), "1")

        grammar_temp.close()


    def test_generate_hidden(self):

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

        with open(grammar_temp.name, 'w') as f:
            f.write(grammar)



        obj = parse_grammar(grammar_temp.name, True)
        create_func(obj, "code_gen_temp2.py", "my_parser", "generated", True)

        import code_gen_temp2

        parser = code_gen_temp2.my_parser

        self.assertEqual(parser.parse("1+1"), (('1', ''), ('+', (('1', ''), ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")

        parser = code_gen_temp2.generated()
        self.assertEqual(parser.parse("1+1"), (('1', ''), ('+', (('1', ''), ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")


        self.assertEqual(parser.parse("1"), (('1', ''), ''))

        grammar_temp.close()



    def test_too_many_starts(self):

        grammar = '''# this is a comments
token plus = "+";
# Grammar;
num = "1";
start = E;
E = T X;
start = T;
T = "(" E ")" | num Y;
X = plus E | "";
Y = "*" T | "";
'''
        self.assertRaises(SemanticError, parse_grammar, grammar)

    def test_no_start(self):

        grammar = '''# this is a comments
token plus = "+";
# Grammar;
num = "1";
E = T X;
T = "(" E ")" | num Y;
X = plus E | "";
Y = "*" T | "";
'''

        self.assertRaises(SemanticError, parse_grammar, grammar)

    def test_only_comments(self):

        grammar = '''#token plus = "+";
#num = "1";
#E = T X;
#T = "(" E ")" | num Y;
#X = plus E | "";
'''
        self.assertRaises(SemanticError, parse_grammar, grammar)


    def test_generated_parser_empty(self):

        grammar = ''''''
        self.assertRaises(SemanticError, parse_grammar, grammar)


    def test_simple_parser(self):

        print("*****************")

        grammar = '''
        start = E;
        num = "1";
        E = T X;
        T = "(" E ")"| num;
        X = "+" E | "";
        '''
        obj = parse_grammar(grammar)
        create_func(obj, "code_gen_temp4.py", "my_parser", "generated", False)

        import code_gen_temp4

        parser = code_gen_temp4.my_parser

        self.assertEqual(parser.parse("1+1"), ('1', ('+', ('1', ''))) )
        self.assertRaises(ParseError, parser.parse, "+1")



        print("*****************")
    def test_multiple_tokens(self):

        grammar = '''token plus = "+";
token plus = "*";
'''
        self.assertRaises(SemanticError, parse_grammar, grammar)

if __name__ == "__main__":
    unittest.main()
