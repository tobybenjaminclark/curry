from typing import Union, List
from Expression import *

class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ""

    def consume(self) -> str:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self) -> LambdaExpr:
        if self.peek() == "λ":
            return self.parse_lambda()
        return self.parse_application()

    def parse_lambda(self) -> LambdaAbstraction:
        self.consume()  # consume 'λ'
        params = []
        while self.peek() and (self.peek().isalnum() or "." in self.peek() or "₁" <= self.peek() <= "₉₀"):
            params.append(Variable(self.consume()))
        print(f"params: {params}")
        if self.consume() != "→":
            raise SyntaxError("Expected → in lambda abstraction")
        body = self.parse()
        return LambdaAbstraction(params, body)
    
    def parse_application(self) -> LambdaExpr:
        exprs = []
        while self.peek() and self.peek() != ")":
            if self.peek() == "(":
                self.consume()  # consume '('
                exprs.append(self.parse_application())
                self.consume()  # consume ')'
            else:
                exprs.append(Variable(self.consume()))
        if len(exprs) == 1:
            return exprs[0]
        return FunctionApplication(exprs[0], exprs[1:])