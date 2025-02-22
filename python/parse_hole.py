from fill_holes import get_holes


def parse_hole(hole_str):
    print("PARSING", hole_str)




if __name__ == "__main__":
    file_name = "calculus/test_one.agda"
    holes = get_holes(file_name)
    for hole in holes:
        formula = parse_hole(hole)