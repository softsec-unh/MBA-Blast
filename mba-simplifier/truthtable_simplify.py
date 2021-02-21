#!/usr/bin/python3

"""
simplify the MBA expression by the truth table searching:
    step1: get the entire truth table, then transform it into the linear combination of basis.
    step2: split the MBA expression, replace every bitwise expression with the related basis.
    step3: simplify the MBA expression into the conbination of basis.
    trick: replace the basis with variable, simplify the MBA expression by the sympy library.
"""

import io
import numpy as np
import re
import sympy
import sys
sys.path.append("../tools")
import time
import traceback
import z3
from mba_string_operation import variable_list, verify_mba_unsat, truthtable_expression, truthtable_bitwise, expression_2_term
from commons import get_entire_bitwise


class MBASimplify():
    """
    Attributes:
        vnumber: the number of variable in one expression.
        basisList: the basis vector.
        truthBasisList: the related truth of the basis vector.
        bitTruthList: transform every one truth into the linear combination of the basis.
        middleNameList: in order to simplify the expression by  the temp variable.
    """

    def __init__(self, vnumber, basisList):
        self.vnumber = vnumber
        self.basisList = basisList
        self.truthBasisList = []
        for bit in self.basisList:
            self.truthBasisList.append(truthtable_bitwise(bit, vnumber))
        #transform bitwise to the combination of basis
        self.bitTruthList = self.bit_2_basis()
        #temp variable
        self.middleNameList = []
        for i in range(2 ** self.vnumber):
            vname = "X{num}".format(num=i)
            self.middleNameList.append(vname)
        
        return None


    def bit_2_basis(self):
        """get entire truth table, create the linear combination of every bitwise expression, just store the coefficient of every term.
        Args:
            None
        Returns:
            bitTruthList: the list of basis on every one bitwise expression.
        """
        bitList = get_entire_bitwise(self.vnumber)
        bitTruthList = []

        A = np.mat(self.truthBasisList).T
        for bit in bitList:
            truth = truthtable_bitwise(bit, self.vnumber)
            b = np.mat(truth).T
            resMatrix = np.linalg.solve(A, b)
            resList = np.array(resMatrix).reshape(-1,).tolist()
            resList = [int(i) for i in resList]
            bitTruthList.append(resList)

        return bitTruthList
        


    def simplify(self, mbaExpre):
        """simplify the MBA expression.
        Algorithm:
            step1: split the expression into list of terms.
            step2: for every term, split the term into coeffcient and bitwise expression.
            step3: for the bitwise, transform it into linear combination of temp variable name.
            step4: construct every term into the multiplication of temp variable name.
            step5: goto step2, until loop end.
            step6: apply sympy to simplify the transformation.
            step7: replace the temp variable name with bitwise expression in the simplified expression.
        Arg:
            mbaExpre: MBA expression.
        Return:
            resExpre: the related simplified MBA expression.
        """
        #split the expression into terms
        termList = expression_2_term(mbaExpre)
        newtermList = []
        for term in termList:
            #split the term
            itemList = re.split("\*", term)
            #the term is constant
            if len(itemList) == 1:
                if not re.search("[a-z]", itemList[0]):
                    coe = int(itemList[0])
                    if coe < 0:
                        coeStr = "+{coe}".format(coe=abs(coe))
                        itemList = [coeStr, "~(x&~x)"]
                    elif coe > 0:
                        coeStr = "-{coe}".format(coe=coe)
                        itemList = [coeStr, "~(x&~x)"]
            #get the coefficient
            coe = itemList[0]
            if not re.search("\d", coe):
                itemList.insert(0, "")
                if coe[0] == "-":
                    coe = "-1"
                else:
                    coe = "+1"
            bitTransList = []
            #transform every bitwise expression into linear combination of basis
            for bit in itemList[1:]:
                truth = truthtable_bitwise(bit, self.vnumber)
                #get the index of truth table
                index = 0
                for (idx, value) in enumerate(truth):
                    index += value *  2**idx
                #transform the truth table to the related basis
                basisVec = self.bitTruthList[index]
                basisStrList = []
                for (idx, value) in enumerate(basisVec):
                    if value < 0:
                        basisStrList.append(str(value) + "*" + self.middleNameList[idx]) 
                    elif value > 0:
                        basisStrList.append("+" + str(value) + "*" + self.middleNameList[idx]) 
                #construct one bitwise transformation 
                basisStr = "".join(basisStrList)
                if basisStr:
                    if basisStr[0] == "+":
                        basisStr = basisStr[1:]
                    #one bitwise transformation
                    bitTransList.append("({basis})".format(basis=basisStr))
            #not zero 
            if bitTransList:
                #construct the entire term.
                bitTrans = "*".join(bitTransList)
                #contain coefficient
                bitTrans = coe + "*" + bitTrans
                newtermList.append(bitTrans)
        #construct the transformation temp result
        midExpre = "".join(newtermList)
        #simplify the temp result, but must process the power operator
        resExpre = self.sympy_simplify(midExpre)
        resExpre = resExpre.strip()
        resExpre = resExpre.replace(" ", "")
        resExpre = self.power_expand(resExpre)
        #replace the temp variable name with real bitwise expression
        #for (idx, var) in enumerate(self.middleNameList):
        for idx in range(len(self.middleNameList)-1, -1, -1):
            var = self.middleNameList[idx]
            basis = self.basisList[idx]
            resExpre = resExpre.replace(var, basis)

        #verification
        z3res = verify_mba_unsat(mbaExpre, resExpre)
        if not z3res:
            print("error in simplify MBA expression.")
            sys.exit(0)

        return resExpre


    def sympy_simplify(self, mbaExpre):
        """simplify the mba expression by the sympy library.
        Args:
            mbaExpre: the mba expression.
        Returns:
            newmbaExpre: the simplified mba expression.
        """
        #variable symbols
        if self.vnumber in [1, 2, 3, 4]:
            X0 = sympy.symbols("X0")
            X1 = sympy.symbols("X1")
            X2 = sympy.symbols("X2")
            X3 = sympy.symbols("X3")
            X4 = sympy.symbols("X4")
            X5 = sympy.symbols("X5")
            X6 = sympy.symbols("X6")
            X7 = sympy.symbols("X7")
            X8 = sympy.symbols("X8")
            X9 = sympy.symbols("X9")
            X10 = sympy.symbols("X10")
            X11 = sympy.symbols("X11")
            X12 = sympy.symbols("X12")
            X13 = sympy.symbols("X13")
            X14 = sympy.symbols("X14")
            X15 = sympy.symbols("X15")
        else:
            print("error in sympy_simplify")
            sys.exit(0)
        #simplify it
        resExpre = sympy.simplify(eval(mbaExpre))
        #output the result to a variable
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        print(resExpre, end="")
        newmbaExpre = new_stdout.getvalue()
        sys.stdout = old_stdout

        return newmbaExpre


    def power_expand(self, mbaExpre):
        """since the sympy simplification expression contains power operator, which is unaccepted by solver,we expand the power operator.
        Args:
            mbaExpre: mba expression.
        Returns:
            newmbaExpre: the expanded mba expression.
        """
        #split the expression by power operator.
        itemList = re.split("(\*\*)", mbaExpre)

        breakFlag = False
        for (idx, item) in enumerate(itemList):
            if r"**" in item:
                #pre/post-item of the power operator
                preStr = itemList[idx - 1]
                postStr = itemList[idx + 1]
                #get the one operand of power operator -- variable name
                splitList = re.split("\*", preStr)
                splitList = re.split("[\+-]", splitList[-1])
                varName = splitList[-1]
                #get the one operand of power operator -- value
                count = ""
                for (i, c) in enumerate(postStr):
                    #the beginning character must be a number
                    if re.search("\d", c):
                        count += c
                    else:
                        breakFlag = True
                        break
                count = int(count)
                #remove the value from the postStr
                if breakFlag:
                    itemList[idx + 1] = itemList[idx + 1][i:]
                    breakFlag = False
                else:
                    itemList[idx + 1] = itemList[idx + 1][i+1:]
                    breakFlag = False
                #expand the power operator
                #the number of 1 is because the preStr have one variable name
                powerList = [varName] * (count - 1)
                powerStr = "*" + "*".join(powerList)
                #replace the power operator with proper expression
                itemList[idx] = powerStr
            else:
                continue

        newmbaExpre = "".join(itemList)

        return newmbaExpre


def refine_simplification(resultVector, vnumber):
    """after get the result vector, refine the result expression.
    Args:
        resultVector: the result vector of the mba expression.
        vnumber: the number of variables in the expression.
    Return:
        (True, simExpre): sucessfully refine the result expression.
        (False,): the result expression can't be refined.
    Raise:
        None.
    """
    truthtableList = get_entire_bitwise(vnumber)

    #refine the simplification result
    resultSet = set(resultVector)
    if len(resultSet) == 1:
        coefficient = resultSet.pop()
        if coefficient == 0:
            print("vector calculation error!")
            traceback.print_stack()
            sys.exit(0)
        else:
            simExpre = str(-1 * coefficient)
            return (True, simExpre)
    elif len(resultSet) == 2 and (0 in resultSet):
        coefficient = resultSet.pop()
        if coefficient == 0:
            coefficient = resultSet.pop()
            if coefficient == 0:
                print("vector calculation error!")
                traceback.print_stack()
                sys.exit(0)
        index = 0
        for i in range(len(resultVector)):
            if resultVector[i]:
                index += 2**i
        simExpre = str(coefficient) + "*" + truthtableList[index]
        return (True, simExpre)
    else:
        return (False, )


def refine_mba(mbaExpre, vnumber):
    """after simplification, refine the simplified expression.
    Args:
        mbaExpre: the expression after simplification.
        vnumber: the number of variable in the mba expression.
    Returns:
        resList[1]: the new expression after refining.
        mbaExpre: cannot be refined, return the orignal mba expression.
    """
    truthList = truthtable_expression(mbaExpre, vnumber)
    resList = refine_simplification(truthList, vnumber)

    if resList[0]:
        return resList[1]
    else:
        return mbaExpre


def simplify_MBA(mbaExpre):
    """simplify a MBA expression.
    Args:
        mbaExpre: a MBA expression.
    Returns:
        simExpre: a expression after simplification.
        vnumber: the nubmer of variable in the mba expression.
        replaceStr: the variable name replacement relationship since our program only process the expression containing "x,y,z" variable.
    """
    basisVec2 = ["x", "y", "(x&y)", "~(x&~x)"]
    basisVec3 = ["x", "y", "z", "(x&y)",  "(y&z)", "(x&z)", "(x&y&z)", "~(x&~x)"]

    if re.search("x", mbaExpre) or re.search("y", mbaExpre) or re.search("z", mbaExpre) or re.search("t", mbaExpre):
        vnumber = 2
        nmbaExpre = mbaExpre.replace("z", "x").replace("t", "y")
        psObj = MBASimplify(vnumber, basisVec2)
        simExpre = psObj.simplify(nmbaExpre)
        if re.search("z", mbaExpre) or re.search("t", mbaExpre):
            return (simExpre, vnumber, "zt")
        else:
            return (simExpre, vnumber, "xy")

    else:
        vnumber = 3
        nmbaExpre = mbaExpre.replace("a", "x").replace("b", "y").replace("c", "z")
        nmbaExpre = nmbaExpre.replace("d", "x").replace("e", "y").replace("f", "z")
        psObj = MBASimplify(vnumber, basisVec3)
        simExpre = psObj.simplify(nmbaExpre)
        if re.search("a", mbaExpre):
            return (simExpre, vnumber, "abc")
        else:
            return (simExpre, vnumber, "def")




def simplify_dataset(datafile):
    """simplify the expression storing in the file.
    Args:
        datafile: the file storing linear MBA expression.
    Return:
        None
    """
    filewrite = "{source}.truthtable.search.simplify.txt".format(source=datafile)

    fw = open(filewrite, "w")
    print("complex,groundtruth,simplified,z3flag", file=fw)

    with open(datafile, "rt") as fr:
        for line in fr:
            if "#" not in line:
                line = line.strip()
                line = line.replace(" ", "")
                itemList = re.split(",", line)
                cmbaExpre = itemList[0]
                groundtruth = itemList[1]
                (simExpre, vnumber, replaceStr) = simplify_MBA(cmbaExpre)
                simExpre = refine_mba(simExpre, vnumber)
                if len(replaceStr) == 2:
                    simExpre = simExpre.replace("x", replaceStr[0]).replace("y", replaceStr[1])
                elif len(replaceStr) == 3:
                    simExpre = simExpre.replace("x", replaceStr[0]).replace("y", replaceStr[1]).replace("z", replaceStr[2])
                else:
                    print("bug in simplify_dataset")
                print("complex MBA expression: ", cmbaExpre)
                print("after simplification:   ", simExpre)
                print("z3 checking...")
                z3res = verify_mba_unsat(groundtruth, simExpre, 8)
                if not z3res:
                    print("z3 solved: ", z3res, line, cmbaExpre, simExpre)
                else:
                    print("z3 solved: ", z3res)
                print(cmbaExpre, groundtruth, simExpre, z3res, sep=",", file=fw)

    fw.close()
    return None



def unittest(fileread, vnumber):
    simplify_dataset(fileread, vnumber)

    return None



if __name__ == "__main__":
    fileread = sys.argv[1]
    simplify_dataset(fileread)
    #unittest()



