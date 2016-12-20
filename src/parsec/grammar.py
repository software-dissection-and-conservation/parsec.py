#=================================================================
# Grammar
#=================================================================
from parsec import *
from parsec.ast import *

def many_of(s):
    return many(one_of(s))
