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

process_comment = lambda s: Comment(array_to_string(s).strip())
comment = (symbol("#") >> many(none_of("\n")) << whitespace).parsecmap(process_comment)

identifier = trim(regex("[a-zA-Z_][0-9a-zA-Z_]*")).parsecmap(array_to_string)
start = (symbol("start") >> symbol("=") >> identifier << symbol(";")).parsecmap(Start)
