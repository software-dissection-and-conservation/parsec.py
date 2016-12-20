#=================================================================
# Abstract Syntax Tree
#=================================================================

class Node:
    def __repr__(self):
        return "<{0}>".format(self)

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
        return "token {0} = \"{1}\";".format(self.name, self.value)

