from parsec.ast import *

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def validate_ast(ast):
    tokens = ast.tokens();
    rules = ast.rules();
    token_names = list(map(lambda token: token.name, tokens))
    rule_names = list(map(lambda rule: rule.name, rules))
    names = token_names + rule_names

    for name in token_names:
        if token_names.count(name) > 1:
            raise SemanticError("'" + name + "' already defined as token")
        if rule_names.count(name) > 0:
            raise SemanticError("'" + name + "' already defined as rule")

    for name in rule_names:
        if token_names.count(name) > 0:
            raise SemanticError("'" + name + "' already defined as token")
        if rule_names.count(name) > 1:
            raise SemanticError("'" + name + "' already defined as rule")

    for rule in rules:
        for production in rule.productions:
            for part in production.parts:
                if isinstance(part, Identifier) and names.count(part.name) == 0:
                    raise SemanticError("'" + name + "' is not defined")


    return True




