#=================================================================
# Abstract Syntax Tree
#=================================================================

class Comment:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "# {0}".format(self.message)

    def __repr__(self):
        return "<{0}>".format(self)

class Start:
    def __init__(self, start_rule):
        self.start_rule = start_rule

    def __str__(self):
        return "start = {0};".format(self.start_rule)

    def __repr__(self):
        return "<{0}>".format(self)
