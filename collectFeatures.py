import feature_extractor
import pe_parser
import os
from ctypes import *
import numpy as np

"""collectNGrams(filepath,ngramSize,ngramCount)
Collects ngram values from all files in the given directory and returns the ngramCount most common ngrams.
"""
def collectTopNGrams(filepath,ngramSize,ngramCount):
    #TODO path to nsort.so
    path = r'C:\Users\Martin\Desktop\Anti-malware-tool\Anti-malware-tool\nsort.so'
    libObject = CDLL(path)
    nsort = libObject.findNTopValues
    nsort.argtypes = [c_int, POINTER(c_uint16), c_uint32]
    nsort.restype = POINTER(POINTER(c_uint32))
    arr = (c_uint16 * 4294967296)()
    arrPtr = pointer(arr)
    ntopValues = POINTER(POINTER(c_uint16))
    
    mypath = filepath
    # collect all ngram values 
    for file in os.listdir(mypath):
        print('Collecting values from file:',file)
        values = feature_extractor.getNgram(f"{filepath}\\{file}",ngramSize)
        for x in values:
            arrPtr.contents[x] = c_uint16(arrPtr.contents[x]+1)

        print('Values were collected...')
    print("Sorting is happening ...")
    # replace with C func
    ntopValues = nsort(c_int(ngramCount),arrPtr.contents,4294967295)
    # 
    print("DONE :)")
    result = []
    for x in range(ngramCount):
        result.append(ntopValues[x].contents.value)
    
    return result

"""collectCallsDump(filepath,count)
This method will collect the most common calls from the given directory. It will return the <count> most common calls.
"""
def collectTopCallsDump(filepath,count):
    result = dict()
    for file in os.listdir(filepath):
        print('Collecting values from file:',file)
        element = pe_parser.createObject(f"{filepath}\\{file}")
        callDump = feature_extractor.getCallsDump(element.getCode())
        for x in callDump:
            if x in result:
                result[x] += 1
            else:
                result.append(x,1)
                
    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:count]
        
    
"""method
Methods collectNGrams and collectCallsDumps have to be used with positive and negative samples separately. Then 
collected features from positive samples will be removed from negative feature set.
"""


def filterNGrams(file,posNgrams):
    result = []
    values = feature_extractor.getNgram(file,4)
    result.append([x for x in values if x in posNgrams])
    return result

def filterCallsDump(code,posCalls):
    result = []
    callDump = feature_extractor.getCallsDump(code)
    result.append([x for x in callDump if x in posCalls])
    return result

def collectFeatures(filePath,posNgrams,posCalls):
    result = []
    for file in os.listdir(filePath):
        print('Collecting values from file:',file)
        element = pe_parser.createObject(f"{filePath}\\{file}")
        code = element.getCode()
        imports = element.getImports()
        tampered = element.getTampered()
        packed = element.getPacked()
        insRatio = feature_extractor.getInstRatio(code)
        ngram = filterNGrams(feature_extractor.getNgram(code,4))
        callsDump = filterCallsDump(feature_extractor.getCallsDump(code))
        result.append([ngram,callsDump,insRatio,imports,tampered,packed])
# topNGrams = collectNGrams('C:\\Users\\Martin\\Desktop\\Samples',4,50)
# print(collectCallsDump('C:\\Users\\Martin\\Desktop\\Samples',50))



