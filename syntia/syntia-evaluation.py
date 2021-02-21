#!/usr/bin/python2

import re
import sys
import time


def verify_mba_expression(leftExpre, rightExpre, bitnumber=2):
    """check the relaion whether the left expression is euqal to the right expression.
    Args:
        leftExpre: left expression.
        rightExpre: right expression.
        bitnumber: the number of the bits of the variable.
    Returns:
        True: equation.
        False: unequal.
    Raises:
        None.
    """
    x,y,z,t,a,b,c,d,e,f = z3.BitVecs("x y z t a b c d e f", bitnumber)

    leftEval = eval(leftExpre)
    rightEval = eval(rightExpre)

    solver = z3.Solver()
    solver.add(leftEval != rightEval)
    result = solver.check()

    if str(result) != "unsat":
        return False
    else:
        return True



def SimpCheck(simExpreStr):
    """check the expression whether obtain the special operator: <<, >>, %, ++,/....
    Args:
        simExpreStr: the expression string.
    Return:
        True/False
    Raise:
        None.
    """
    if re.search(r"<<", simExpreStr):
        return False
    elif re.search(r">>", simExpreStr):
        return False
    elif re.search(r"\+\+", simExpreStr):
        return False
    elif re.search(r"/", simExpreStr):
        return False
    elif re.search(r"%", simExpreStr):
        return False
    elif re.search(r"sign_ext", simExpreStr):
        return False
    elif re.search(r"zero_ext", simExpreStr):
        return False
    elif re.search(r"extract", simExpreStr):
        return False
    else:
        return True

    return None



def SyntiaEvaluation(bitNum, readfilename, writefilename):
    """do the syntia evaluation
    Args:
        bitNum: the bit number of the variables.
        readfilename: from this file read the expression.
        writefilename: write the results to this file.
    Return:
        None.
    Raise:
        None.
    """
    fwrite = open(writefilename, "w")

    fwrite.write("#original,correct,simplified,simplificationTrue/False,z3time\n")

    with open(readfilename, "r") as data:
        for line in data:
            line = line.replace("\n", "")
            resultStr = line

            if line[0] != "#" and line:
                expreStrList = re.split(",", line)
                sourceExpreStr = expreStrList[0]
                correctExpreStr = expreStrList[1]
                simExpreStr = expreStrList[2]
                #z3 check the simplification results.
                if SimpCheck(simExpreStr):
                    #get the nodes and alternance of the expression.
                    start = time.time()
                    z3Result = verify_mba_expression(simExpreStr, correctExpreStr, bitNum)
                    end = time.time()
                    elapsed = end - start
                    resultStr += "," + str(z3Result) + "," + str(elapsed) + "\n"
                else:
                    resultStr += ",0,0,0,0"
                    resultStr += "," + "False" + "," + str(0) + "\n"
                fwrite.write(resultStr)
            elif line[0] == "#" and line[1] == "#":
                fwrite.write(line + "\n")
            fwrite.flush
    
    fwrite.close()
    return None



def main(bitNum, readfilename, writefilename):
    SyntiaEvaluation(bitNum, readfilename, writefilename)



if __name__ == "__main__":
    bitNum = int(sys.argv[1])
    readfilename = sys.argv[2]
    writefilename = sys.argv[3]
    main(bitNum, readfilename, writefilename)



