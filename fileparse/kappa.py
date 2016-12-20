from __future__ import generators
import string
from parsec import *

@generate
def plus():
    yield (string("+"))
@generate
def T():
    yield ((string("(") + E + string(")") ) ^ (num + Y ) )
@generate
def Y():
    yield ((string("*") + T ) ^ (string("") ) )
@generate
def X():
    yield ((plus + E ) ^ (string("") ) )
@generate
def E():
    yield ((T + X ) )
@generate
def Start():
    yield (E + eof())
