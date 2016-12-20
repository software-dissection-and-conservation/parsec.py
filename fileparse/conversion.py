#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import generators

"""
Test the specification of parsec.py.
"""

__author__ = "Daniel Edin, Micael Loberg and Tommy Vagbratt"

import random
import string
import unittest
from parsec import *


skip_blanks = many1(string(" "))
_skip_blanks = many(string(" "))



def List_to_String(lis,separator=''):
    return separator.join(lis)

def Tup_to_String(lis,separator=''):

    return separator.join(lis)


epsilon = string("").result("EPSILON")

equals = _skip_blanks >> string("=") << _skip_blanks

pipe = _skip_blanks >> string("||") << _skip_blanks

#token = (caseless_string("ToKEN") >> skip_blanks >> many(letter())).parsecmap(List_to_String)


def production_parser():

    #use word to identify the rule name
    word = _skip_blanks >>  many1(string('""')^letter()^digit()).parsecmap(List_to_String)

    #up until equals
    production = word << equals

    anything = many1(none_of('"')).parsecmap(List_to_String)
    #KAPPA vad fint
    string_parser = ((string('"') + anything).parsecmap(List_to_String) + string('"')).parsecmap(List_to_String)

    word = word ^ string_parser
    word = word << (_skip_blanks)
    production = production + sepBy1(many1(word), pipe)

    return production


def comment():
    comment = _skip_blanks >> (string("#") + (eof() ^ many(any_char())).parsecmap(List_to_String))
    return comment


def start():
    start = _skip_blanks >> caseless_string("start") << equals
    start = start + many1(letter()^digit()) << _skip_blanks

    #eof() puts it in another list??? wtf
    #start = start << eof()
    return start


def token():
        #TODO regex

        #token = (_skip_blanks >> caseless_string("ToKEN") >> _skip_blanks >> many(letter())).parsecmap(List_to_String)

        token = _skip_blanks >> caseless_string("token")

        token = token + (skip_blanks >> many1(letter()^digit()).parsecmap(List_to_String))

        anything = many1(none_of('"')).parsecmap(List_to_String)
        string_parser = ((string('"') + anything).parsecmap(List_to_String) + string('"')).parsecmap(List_to_String)

        token = token + (equals >> string_parser)

        return token


def gen_string(s):
    return (string("(") + string(s) + string(")"))



start_rule = [] 

rules = {}
tokens = {}

productions = {}

comments = []



# def rule():

# def production():

# dictionary



#http://stackoverflow.com/questions/11815503/whats-the-best-way-to-write-python-code-into-a-python-file
class CodeBlock():
    def __init__(self, head, block):
        self.head = head
        self.block = block
    def __str__(self):
        return self.convert_to_string()

    def convert_to_string(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, CodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result

preemble = '''from __future__ import generators
import string
from parsec import *

'''

def line_master(funcname, yielder):
    return CodeBlock('@generate\ndef '+ funcname + '()', ['yield ('+yielder+')'])

def create_func():

   # funcname = 'Start'
   # yielder = 'E << eof()'


    with open("kappa.py", 'w') as f:
        f.write(preemble)
        for key in tokens:
            f.write(line_master(key, tokens[key]).convert_to_string())

        for key in rules:
            f.write(line_master(key, rules[key]).convert_to_string())

        f.write(line_master("Start", start_rule[0]+' + eof()').convert_to_string())

    print("kappa done")


def parse_grammar(filename):
    start_parser   = start()
    rule_parser    = production_parser()
    comment_parser = comment()
    token_parser   = token()

    with open(filename, 'r') as f:
        for line in f:
            linenumber = 1
            parsed = (comment_parser ^ start_parser ^ rule_parser ^ token_parser).parse(line)
            print(parsed)

            if len(parsed[0]) == 2 :
                key = parsed[0][1]
                if key not in tokens:
                    tokens[key] = 'string('+parsed[1]+')'
                    print(key+': '+tokens[key])
                else:
                    print(key+" was in tokens")


            elif parsed[0] == '#':
                comments.append((linenumber, parsed[1]))

            elif parsed[0] == 'start':
                start_rule.append(parsed[1][0])
                print(parsed[1])


            else:
                if parsed[0] in tokens:
                    print("rule / prod same name as token")
                elif parsed[0] not in rules:
                    rule = ""
                    i = 0
                    for production in parsed[1]:
                        i+=1

                        j = 0
                        for construct in production:
                            if j == 0:
                                rule += '('
                            j+=1
                            if construct[0] == '"':
                                rule += 'string('+construct+') '
                            else:
                                rule += construct + ' '
                            if j < len(production):
                                rule += '+ '

                            if j == len(production):
                                rule += ') '

                        if i < len(parsed[1]):
                            rule += '^ '



                    print(rule)
                    rules[parsed[0]] = rule



            linenumber+=1





@generate
def Start():
    yield (E << eof())

@generate
def E():
    #print("E")
    yield (T + X)
    #return ret

@generate
def T():
    #print("T")
    yield ( (string("(") + E + string(")")) ^ (digit() + Y) )

@generate
def X():
    #print("X")
    yield ( (string("+") + E) ^ epsilon)

@generate
def Y():
    #print("Y")
    yield ( (string("*") + T) ^ epsilon)



def aggregate_token_parsers():

    #pretty function, Kappa

    parser = None

    for key, value in tokens.items():
        if parser != None:
            parser = parser ^ value
        else:
            parser = value

    return parser


class simple_test(unittest.TestCase):

    def test_parse(self):
        parse_grammar("kappa.txt")
        create_func()

    def _test_token(self):
        print(token().parse('token plus = "+"'))



    def _test_start(self):
        print(start().parse("start = E"))

    def _test_generate(self):
        create_func()


    def _test_start(self):
        start = _skip_blanks >> caseless_string("start") << equals
        start = start + many1(letter()^digit()).parsecmap(List_to_String)
        start = start << (_skip_blanks << eof())

        print(start.parse("   start    =      E      "))



    def _test_comment(self):
        comment = _skip_blanks >> (string("#") + (eof() ^ many(any_char())))

        print(comment.parse("#    kappakdhasdask¤%&(%/¤"))


    def _test_rule2(self):
        print(production_parser().parse('Y = "*" T || ""'))

    def _test_rule(self):



        #use word to identify the rule name
        word = _skip_blanks >>  many1(letter()^digit()).parsecmap(List_to_String)

        #up until equals
        production = word << equals


        #reuse word to identify either a rule or production
        #TODO anything
        #anything = one_of("()")
        #TODO how to allow multiple characters? Will many conflict with end?
        anything = many1(none_of('"')).parsecmap(List_to_String)


        #KAPPA vad fint
        string_parser = ((string('"') + anything).parsecmap(List_to_String) + string('"')).parsecmap(List_to_String)


        word = word ^ string_parser

        word = word << (_skip_blanks)

        #production2 = production + many1(word) + many(pipe + many1(word))


        production2 = production + many(many1(word) ^ pipe)

        production3 = production + sepBy1(many1(word), pipe)

        #many1(word) + many(pipe + many1(word))



        production = production + many1(word) + many(pipe + word)





        res = production.parse("kappa = plus keff || keff")
        print(res)

 
        print(production.parse('''T = "(" E ")" || num Y'''))
        print(production3.parse('''T = "(" E ")" ||num Y || num X|| num F|| num Y'''))
       # if res[1][0] in tokens:
       #     print("production! Kappa")
       #     productions[res[0]] = res[1]
       # else:
       #     print("Rule! Kappa")
       #     rules[res[0]] = res[1]






        #self.assertEqual((string("x")+string("y")).parse("xy"), "y")

    def _test_aggregate_tokens(self):

        tokens = {
        "plus": string("+"),
        "times": string("*")
        }


        parser = aggregate_token_parsers()
        self.assertEqual(parser.parse("+"), "+")
        self.assertEqual(parser.parse("*"), "*")
        self.assertEqual(many(parser).parse("*+"), ['*', '+'])
        #self.assertEqual((string("x")+string("y")).parse("xy"), "y")


    def test_kappa(self):

        print(Start.parse("1+2"))
        #self.assertEqual(Start.parse("1+2"), "x")

        #self.assertEqual((string("x")+string("y")).parse("xy"), "y")



    def _test_regex(self):


        regx = re.compile(r"[a-z]")
        test = regex(regx)
        print( test.parse("kappa"))

        token = (caseless_string("ToKEN") >> _skip_blanks >> many(letter())).parsecmap(List_to_String)

        #anything_regex = (skip_blanks >> many(one_of(""".^$*+?{}\[]|#<>=!-"'""") ^ letter()))

        anything_regex_conc = (_skip_blanks >> (string("r") ^ string('\\')))+(many(one_of(""".^$*+?{}\[]|#<>=!-"'""") ^ letter())).parsecmap(List_to_String)

        anything_regex_conc = anything_regex_conc.parsecmap(List_to_String)

        parser = token + (skip_blanks >> string("=")) + many1(skip_blanks >> ((anything_regex_conc) ^ string("||")))

        #< (many(string("")) | string("="))


        self.assertEqual(parser.parse("""ToKen kappa = r"[a]" || "lol" """ ), "kappa")

        self.assertRaises(ParseError, parser.parse, "")
        #self.assertEqual(parser.parse("ToKen kappa ="), "kappa")
        self.assertRaises(ParseError, parser.parse, " xxx")


if __name__ == "__main__":
    unittest.main()
