#!/usr/bin/python2

from collections import OrderedDict
import json
import re
import sys

    
def TransforExpre(simExpreStr):
    """transformate the result to format result.
    Args:
        simExpreStr: expression string.
    Returns:
        expreStr: new expression string.
    Raise:
        None.
    """
    expreStr = simExpreStr
    expreStr = expreStr.replace("mem0", "x")
    expreStr = expreStr.replace("mem1", "y")
    expreStr = expreStr.replace("mem2", "z")
    expreStr = expreStr.replace("mem3", "t")
    expreStr = expreStr.replace("mem4", "a")
    expreStr = expreStr.replace("mem5", "b")
    expreStr = expreStr.replace("mem6", "c")
    expreStr = expreStr.replace("mem7", "d")
    expreStr = expreStr.replace("mem8", "e")
    expreStr = expreStr.replace("mem9", "f")
    #dont process the special operator
    #in the check process, it directly is wrong!
    """
    if re.search("<<", expreStr):
        obj = re.search("<<", expreStr)
        index = obj.span()[0]
        starStr = expreStr[index:index + 4]
        expreStr = expreStr.replace(starStr, "*(2**" + expreStr[index + 3] + ")")
    elif re.search(">>", expreStr):
        obj = re.search(">>", expreStr)
        index = obj.span()[0]
        starStr = expreStr[index:index + 4]
        expreStr = expreStr.replace(starStr, "/(2**" + expreStr[index + 3] + ")")
    """
    return expreStr
    
def transformation(sourcefile, desfile):    
    """transformate the json result to format result.
    Args:
        sourcefile: the source json file.
        desfile: the file store the result.
    Return:
        None.
    Raise:
        None.
    """
    jsonDict = {}
    with open(sourcefile, "r") as data:
        jsonDict = json.load(data)

    alltime = jsonDict["0"]
    del jsonDict["0"]

    fwrite = open(desfile, "w")
    fwrite.write("#original,correct,simplified\n")
    fwrite.write("##all synthesis time:" + alltime + "\n")

    #let the dictionary be ordered.
    dataDict1 = OrderedDict()
    for (key, value) in jsonDict.items():
        dataDict1[int(key)] = jsonDict[key]
    del jsonDict

    keys = sorted(dataDict1.keys())
    dataDict = OrderedDict()
    for key in keys:
        dataDict[key] = dataDict1[key]
    del dataDict1

    for (key, value) in dataDict.items():
        sourceExpreStr = value["orignalExpression"]
        correctExpreStr = value["correctExpression"]
        simExpreStr = value["top_terminal"]["expression"]["infix"]
        simExpreStr = TransforExpre(simExpreStr)
        expreStr = sourceExpreStr + "," + correctExpreStr
        expreStr += "," + simExpreStr + "\n"
        fwrite.write(expreStr)
        
    fwrite.close()
        


def main(sourcefile, desfile):
    transformation(sourcefile, desfile)



if __name__ == "__main__":
    sourcefile = sys.argv[1]
    desfile = sys.argv[2]
    main(sourcefile, desfile)
