from typing import Union, List

class LambdaExpr:
    pass

class Variable(LambdaExpr):
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return self.name

class LambdaAbstraction(LambdaExpr):
    def __init__(self, param: Variable, body: LambdaExpr):
        self.param = param
        self.body = body
    
    def __repr__(self):
        return f"λ{self.param}. {self.body}"

class FunctionApplication(LambdaExpr):
    def __init__(self, func: LambdaExpr, args: List[LambdaExpr]):
        self.func = func
        self.args = args
    
    def __repr__(self):
        return f"({self.func} {' '.join(map(str, self.args))})"