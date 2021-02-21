#!/usr/bin/python2

import json
import random
import re
import sys
import time
import os

def JsonHead(bitNum):
    """build the json file head to meet the requirement of MCTS synthesis method.
    Args:
        bitNum: the number of the bits of variables.
    Returns:
        jsonDict.
    Raise:
        None.
    """
    jsonDict = {}

    sizeStr = str(bitNum / 8)

    #the symbol x information
    itemDict0 = {}
    itemDict0["location"] = "mem0"
    itemDict0["size"] = sizeStr
    #the symbol y information
    itemDict1 = {}
    itemDict1["location"] = "mem1"
    itemDict1["size"] = sizeStr
    #the symbol z information
    itemDict2 = {}
    itemDict2["location"] = "mem2"
    itemDict2["size"] = sizeStr
    #the symbol t information
    itemDict9 = {}
    itemDict9["location"] = "mem3"
    itemDict9["size"] = sizeStr
    #the symbol a information
    itemDict3 = {}
    itemDict3["location"] = "mem4"
    itemDict3["size"] = sizeStr
    #the symbol b information
    itemDict4 = {}
    itemDict4["location"] = "mem5"
    itemDict4["size"] = sizeStr
    #the symbol c information
    itemDict5 = {}
    itemDict5["location"] = "mem6"
    itemDict5["size"] = sizeStr
    #the symbol d information
    itemDict6 = {}
    itemDict6["location"] = "mem7"
    itemDict6["size"] = sizeStr
    #the symbol e information
    itemDict7 = {}
    itemDict7["location"] = "mem8"
    itemDict7["size"] = sizeStr
    #the symbol f information
    itemDict8 = {}
    itemDict8["location"] = "mem9"
    itemDict8["size"] = sizeStr
    #inputs information
    inputDict = {}
    inputDict["0"] = itemDict0 
    inputDict["1"] = itemDict1 
    inputDict["2"] = itemDict2 
    inputDict["3"] = itemDict3 
    inputDict["4"] = itemDict4 
    inputDict["5"] = itemDict5 
    inputDict["6"] = itemDict6 
    inputDict["7"] = itemDict7 
    inputDict["8"] = itemDict8 
    inputDict["9"] = itemDict9 
    jsonDict["inputs"] = inputDict

    #the symbol result information
    itemDict2 = {}
    if bitNum == 8: 
        itemDict2["location"] = "AL"
    if bitNum == 16: 
        itemDict2["location"] = "AX"
    if bitNum == 32: 
        itemDict2["location"] = "EAX"
    if bitNum == 64: 
        itemDict2["location"] = "RAX"
    itemDict2["size"] = sizeStr
    #outputs information
    outputDict = {}
    outputDict["0"] = itemDict2
    jsonDict["outputs"] = outputDict

    return jsonDict


def Sampling(expreStr, number=20, bitNum=32):
    """sampling the I/O pairs based on the expression.
    Args:
        expreStr: the expression string.
    Returns:
        samplingList: the I/O pairs list.
        number: the sampling times.
        bitNum: the number of bits of the variables.
    Raise:
        None.
    """
    samplingList = []

    modNum = 2**bitNum - 1

    for i in range(number):
        item = []

        x = random.randint(0, modNum)
        y = random.randint(0, modNum)
        z = random.randint(0, modNum)
        t = random.randint(0, modNum)
        a = random.randint(0, modNum)
        b = random.randint(0, modNum)
        c = random.randint(0, modNum)
        d = random.randint(0, modNum)
        e = random.randint(0, modNum)
        f = random.randint(0, modNum)
        res = eval(expreStr) % 2**bitNum 

        item.append(str(x))
        item.append(str(y))
        item.append(str(z))
        item.append(str(t))
        item.append(str(a))
        item.append(str(b))
        item.append(str(c))
        item.append(str(d))
        item.append(str(e))
        item.append(str(f))
        item.append(str(res))
        samplingList.append(item)

    return samplingList


def ProgramSynthesis(expreStr, bitNum):
    """synthesizing the semantics of the expression based on the MCTS synthesis method.
        step1: sampling.
        step2: synthesis.
        step3: successful or fail.
    Args:
        expreStr: the expression synthesized.
        bitNum: the number of the bit of the variables.
    Returns:
        None.
    Raises:
        None.
    """
    #sampling json file
    jsonDict = {}
    jsonDict = JsonHead(bitNum)

    #sampling list
    sampleList = Sampling(expreStr, 20, bitNum)
    jsonDict["samples"] = sampleList

    #write the I/O pairs into file
    manuallyfile = str(bitNum) + "bit.manually.json"
    with open(manuallyfile, "w") as f:
        json.dump(jsonDict, f)

    #transform the I/O pairs to meet the requirement of MCTS synthesis program
    samplingfile = str(bitNum) + "bit.sampling.json"
    pythonorder = "python ./mcts_synthesis/transform_manual_sampling_io_pairs.py " + manuallyfile + "  " + samplingfile
    os.system(pythonorder)
    #using the MCTS method to synthesize the MBA expression
    outputfile = str(bitNum) + "bit.output.json"
    pythonorder = "python ./mcts_synthesis/sample_synthesis.py " + samplingfile + " " + outputfile
    os.system(pythonorder)

    return None

def main(bitNum, readfile, desfilename):
    outputfile = str(bitNum) + "bit.output.json"
    resDict = {}
    start = time.time()
    #test this program
    #with open("test.txt", "r") as data:
    with open(readfile, "r") as data:
        linenum = 1
        jsonDict = {}
        for line in data:
            itemDict = {}
            line = line.strip("\n")
            expreStr = ""
            if line and line[0] != "#":
                dataList = re.split(",", line)
                sourceExpreStr = dataList[0]
                correctExpreStr = dataList[1]
                #print linenum, sourceExpreStr
                ProgramSynthesis(sourceExpreStr, bitNum)

                #get result in json format
                with open(outputfile, "r") as f:
                    jsonDict = json.load(f)

                jsonDict["0"]["orignalExpression"] = sourceExpreStr
                jsonDict["0"]["correctExpression"] = correctExpreStr
                resDict[linenum] = jsonDict["0"]

                linenum += 1
                #print 
            
        end = time.time()
        elapsed = end - start
        resDict[0] = str(elapsed) 

        #write the result to file
        with open(desfilename, "w") as fw:
            json.dump(resDict, fw, indent=4)
    


if __name__ == "__main__":
    bitNum = int(sys.argv[1])
    readfile = sys.argv[2]
    desfilename = sys.argv[3]
    main(bitNum, readfile, desfilename)

