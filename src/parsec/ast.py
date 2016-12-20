#=================================================================
# Abstract Syntax Tree
#=================================================================

class Node:
    def __repr__(self):
        return "<{0}>".format(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class String(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "\"{0}\"".format(self.value)

class NameValue(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Comment(Node):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "# {0}".format(self.message)

class Start(Node):
    def __init__(self, start_rule):
        self.start_rule = start_rule

    def __str__(self):
        return "start = {0};".format(self.start_rule)

class Token(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "token {0} = {1};".format(self.name, self.value)

class Production(Node):
    def __init__(self, parts):
        self.parts = parts

    def __str__(self):
        return " ".join(map(str, self.parts))

class Rule(Node):
    def __init__(self, name, productions):
        self.name = name
        self.productions = productions

    def __str__(self):
        return "{0} = {1};".format(self.name, " | ".join(map(str,self.productions)))
