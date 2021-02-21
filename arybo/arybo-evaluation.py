#!/usr/bin/python3


from arybo.lib import MBA
import io
import re
import sys
import time



def arybosimplify(bitnum, sourceExpreStr):
    """simplify the expression by arybo
    Args:
        bitnum: the number of the bit of the variables.
        sourceExpreStr: expression is simplified.
    Returns:
        result: the result after simplification.
    Raise:
        None.
    """
    mba = MBA(bitnum)
    x = mba.var("x")
    y = mba.var("y")
    z = mba.var("z")
    a = mba.var("a")
    b = mba.var("b")
    c = mba.var("c")
    d = mba.var("d")
    e = mba.var("e")
    f = mba.var("f")
    t = mba.var("t")

    res = eval(sourceExpreStr)
    fio = io.StringIO()
    print(res,file=fio)

    result = fio.getvalue()
    fio.close()

    return result




def simplify_file(bitnum, sourcefilename, desfilename):
    fwrite = open(desfilename, "w")
    fwrite.write("#complex,groundtruth,simplified,simfilied time\n")

    with open(sourcefilename, "r") as data:
        linenum = 0 
        for line in data:
            line = line.replace("\n", "")

            if line[0] != "#" and line:
                expreStrList = re.split(",", line)
                sourceExpreStr = expreStrList[0]
                start = time.time()
                simExpreStr = arybosimplify(bitnum, sourceExpreStr)
                end = time.time()
                elapsed = end - start
                simExpreStr = simExpreStr.replace("\n", "")
                print(line, simExpreStr, elapsed, sep=",", file=fwrite, flush=True)
                linenum += 1
    
def main(bitnum, sourcefilename, desfilename):
    simplify_file(bitnum, sourcefilename, desfilename)

if __name__ == "__main__":  
    bitNum = int(sys.argv[1])
    sourcefilename = sys.argv[2]
    desfilename = sys.argv[3]
    main(bitNum, sourcefilename, desfilename)


