#=================================================================
# Abstract Syntax Tree
#=================================================================

class Comment:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "# {0}".format(self.message)
