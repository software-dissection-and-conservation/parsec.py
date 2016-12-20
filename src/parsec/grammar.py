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

# This function was shamelessly stolen from examples/jsonc.py
def charseq():
    """ Parse string. (normal string and escaped string) """
    def string_part():
        """ Parse normal string."""
        return regex(r'[^"\\]+')

    def string_esc():
        """ Parse escaped string."""
        return string('\\') >> (
            string('\\')
            | string('/')
            | string('"').result('"')
            | string('b').result('\b')
            | string('f').result('\f')
            | string('n').result('\n')
            | string('r').result('\r')
            | string('t').result('\t')
            | regex(r'u[0-9a-fA-F]{4}').parsecmap(lambda s: chr(int(s[1:], 16))))
    return string_part() | string_esc()

string_value = (string('"') >> (many(charseq())) << string('"')).parsecmap(lambda s: StringValue(array_to_string(s)))
