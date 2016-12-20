#=================================================================
# Grammar
#=================================================================
from parsec import *
from parsec.ast import *

def many_of(s):
    return many(one_of(s))

def array_to_string(s):
    return "".join(s)

whitespace = many_of(" \n").parsecmap(array_to_string)

def trim(p):
    return whitespace >> p << whitespace

def symbol(s):
    return trim(string(s))
