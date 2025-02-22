import re
from typing import List, Union

from fill_holes import get_holes
from Expression import *

def tokenize(hole_str: str):
    tokens = re.findall(r'[λa-zA-Z₁₂₃₄₅₆₇₈₉₀]+(?:\.[a-zA-Z₁₂₃₄₅₆₇₈₉₀]+)*|\(|\)|→', hole_str)
    return tokens


if __name__ == "__main__":
    file_name = "calculus/test_one.agda"
    holes = get_holes(file_name)
    
    for hole in holes:
        print(f"ORIGINAL STRING: {hole}")
        tokens = tokenize(hole)
        print(f"TOKENS: {tokens}")