import re
from typing import List, Union

from fill_holes import get_holes

class AgdaExpr:
    def __init__(self, name: str, args: List[Union[str, 'AgdaExpr']]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"NAME: {self.name}\n ARGS: {self.args}"

def parse_agda_expression(expr: str) -> AgdaExpr:
    tokens = re.split(r'\s+', expr.strip())
    return _parse_tokens(tokens)

def _parse_tokens(tokens: List[str]) -> AgdaExpr:
    if not tokens:
        return None
    
    name = tokens.pop(0)
    args = []
    
    while tokens:
        token = tokens.pop(0)
        if token.startswith('('):
            sub_expr = [token]
            while tokens and not tokens[0].endswith(')'):
                sub_expr.append(tokens.pop(0))
            if tokens:
                sub_expr.append(tokens.pop(0))
            args.append(parse_agda_expression(' '.join(sub_expr)[1:-1]))
        else:
            args.append(token)
    
    return AgdaExpr(name, args)

def create_hole_struct(hole_str: str):
    return parse_agda_expression(hole_str)

if __name__ == "__main__":
    file_name = "calculus/test_one.agda"
    holes = get_holes(file_name)
    
    for hole in holes:
        print(hole)
        hole_struct = create_hole_struct(hole)
        print(hole_struct)
