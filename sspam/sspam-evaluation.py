#!/usr/bin/python2

import func_timeout
import re
import sspam
from sspam import simplifier
import sys
import time



def sspam_simplify(sourcefilename, desfilename, linethreshold=0):
    timeout = 3600
    desfilename = desfilename  + "." + str(linethreshold) + ".sspam.txt"
    fwrite = open(desfilename, "w")
    fwrite.write("#original,correct,simplified,time\n")
    fwrite.write("#timeout: " + str(timeout) + "s\n")

    with open(sourcefilename) as data:
        linenum = 0
        for line in data:
            line = line.replace("\n","")
            #if line[0] != "#" and line:
            if (line[0] != "#") and (linenum > linethreshold):
                expreStrList = re.split(",", line)
                sourceStr = expreStrList[0]
                start = time.time()
                try:
                    #use func_timeout module:doitreturnvalue=func_timeout(timeout, doit, args)
                    simStr = func_timeout.func_timeout(timeout, simplifier.simplify, args=(sourceStr,))
                except func_timeout.FunctionTimedOut:
                    #enough time to clean the z3 circument.
                    time.sleep(1)
                    resultStr = line
                    resultStr += "," + "timeout\n"
                    fwrite.write(resultStr)
                #except:
                    #print "errors!!"
                else:
                    end = time.time()
                    elapsed = end - start
                    resultStr = line
                    resultStr += "," + simStr + "," + str(elapsed) + "\n"
                    fwrite.write(resultStr)
                fwrite.flush()
                print linenum
                linenum += 1
            elif line[0] != "#" and line:
                linenum += 1
                
    return None

    
def main(sourcefilename, desfilename, linethreshold):
    sspam_simplify(sourcefilename, desfilename, linethreshold)
    


if __name__ == "__main__":
    sourcefilename = sys.argv[1]
    desfilename = sys.argv[2]
    if len(sys.argv) > 3:
        linethreshold = int(sys.argv[3])
    else:
        linethreshold = 0
    main(sourcefilename, desfilename, linethreshold)



