#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the grammar parser
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

from pprint import pprint
from parsec.grammar import *
from parsec.semantic import *


# http://stackoverflow.com/questions/11815503/whats-the-best-way-to-write-python-code-into-a-python-file

class CodeBlock():
    def __init__(self, head, block):
        self.head = head
        self.block = block

    def __str__(self, indent=""):
        return self.convert_to_string(indent)

    def convert_to_string(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, CodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result



class parse_obj:
    def __init__(self):
        self.start_rule = []
        self.comments = []
        self.rules = {}
        self.tokens = {}
        self.productions = {}
        self.preemble = '''from __future__ import generators
import string
from parsec import *


'''


def line_master(funcname, yielder, hide):
    if hide:
        s = '@generate\n    def '
    else:
        s = '@generate\ndef '
    return CodeBlock(s + funcname + '()', ['ret = yield ('+yielder+')', 'return ret\n'])


def create_func(obj, filename, funcname, parsername="generated", hide=True):

    funcs = []

    with open(filename, 'w') as f:
                f.write(obj.preemble)
                for key in obj.tokens:
                    if hide:
                        funcs.append(line_master(key, obj.tokens[key], hide))
                    else:
                        f.write(line_master(key, obj.tokens[key], hide).convert_to_string())

                for key in obj.rules:
                    if hide:
                        funcs.append(line_master(key, obj.rules[key], hide))
                    else:
                        f.write(line_master(key, obj.rules[key], hide).convert_to_string())

                if hide:
                    funcs.append(line_master("start", obj.start_rule[0]+' << eof()', hide))
                    funcs.append('return start')
                    f.write(CodeBlock('def ' + parsername + '()', funcs).convert_to_string())
                    f.write('\n\n' + funcname + ' = ' + parsername + '()')
                else:
                    f.write(line_master("start", obj.start_rule[0]+' << eof()', hide).convert_to_string())
                    f.write('\n\n' + funcname + ' = start')



def parse_grammar(grammar_data, filename=False):

    obj = parse_obj()

    g = None

    if filename:
        with open(grammar_data, 'r') as f:
            data=f.read()
            g = grammar.parse(data)
            validate_ast(g)
    else:
        g = grammar.parse(grammar_data)
        validate_ast(g)

    for token in g.tokens():
        obj.tokens[token.name] = 'string("'+token.value.value+'")'

    for rule in g.rules():
        construct_rule = ""
        i=0
        for prod in rule.productions:
            i+=1
            j=0
            for part in prod.parts:
                if j == 0:
                    construct_rule += '('
                j+=1
                if isinstance(part, String):

                    construct_rule += 'string("'+part.value+'")'
                else:
                    construct_rule += part.name

                if j < len(prod.parts):
                    construct_rule += ' + '
                if j == len(prod.parts):
                    construct_rule += ')'

            if i < len(rule.productions):
                construct_rule += ' ^ '

        obj.rules[rule.name] = construct_rule


    for start in g.starts():
        obj.start_rule.append(start.start_rule)

    return (obj)



