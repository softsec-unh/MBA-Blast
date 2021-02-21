#!/usr/bin/python3



import re
import traceback


def get_entire_bitwise(vnumber):
    """get the entire bitwise expression of 2/3/4-variable.
    Args:
        vnumber: the number of the variables.
    Return:
        bitList: the entire bitwise expression.
    """
    if not vnumber in [1, 2,3,4]:
        print("vnumber must be 1, 2,3 or 4.")
        traceback.print_stack()
        sys.exit(0)
    truthfile = "../dataset/{vnumber}variable_truthtable.txt".format(vnumber=vnumber)
    bitList = []
    with open(truthfile, "r") as fr:
        for line in fr:
            if "#" not in line:
                line = line.strip()
                itemList = re.split(",", line)
                bit = itemList[1]
                bitList.append(bit)

    return bitList



