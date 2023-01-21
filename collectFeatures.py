import feature_extractor
import pe_parser
import os
from ctypes import *
import pandas as pd

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
    
    return set(result)

"""collectCallsDump(filepath,count)
This method will collect the most common calls from the given directory. It will return the <count> most common calls.
"""
def collectTopCallsDump(filepath,count):
    result = dict()
    for file in os.listdir(filepath):
        print('Collecting values from file:',file)
        element = pe_parser.createObject(f"{filepath}\\{file}")
        callDump = feature_extractor.getCallsDump(element.getCode())
        if callDump == None:
            continue
        for x in callDump:
            if x in result:
                result[x] += 1
            else:
                result[x] = 1
                
    # return set(sorted(result.items(), key=lambda x: x[1], reverse=True)[:count])
    return set([key for key, value in sorted(result.items(), key=lambda x: x[1], reverse=True)[:count]])

# def testCollectTopCallsDump(filepath,count):
#     result = dict()
#     for file in os.listdir(filepath):
#         print('Collecting values from file:',file)
#         f = open(f"{filepath}\\{file}")
#         callDump = feature_extractor.testGetCallsDump(f.read().split("\n"))
#         for x in callDump:
#             if x in result:
#                 result[x] += 1
#             else:
#                 result[x] = 1
                
#     return set(sorted(result.items(), key=lambda x: x[1], reverse=True)[:count])
        
    
"""method
Methods collectNGrams and collectCallsDumps have to be used with positive and negative samples separately. Then 
collected features from positive samples will be removed from negative feature set.
"""


def filterNGrams(file,posNgrams):
    result = [0] * len(posNgrams)
    values = feature_extractor.getNgram(file,4)
    intersection = set(posNgrams).intersection(set(values))
    for i in intersection:
        result[posNgrams.index(i)] = 1
    return result #TODO test

def filterCallsDump(code,posCalls):
    result = [0] * len(posCalls)
    callDump = feature_extractor.getCallsDump(code)
    intersection = set(posCalls).intersection(set(callDump))
    for i in intersection:
        result[posCalls.index(i)] = 1
    return result #TODO test

def collectFeatures(filePath, posNgrams, posCalls):
    result = []
    for file in os.listdir(filePath):
        print('Collecting values from file:',file)
        element = pe_parser.createObject(f"{filePath}\\{file}")
        code = element.getCode()
        imports = element.getImports()
        tampered = element.getTampSections()
        packed = element.getPacked()
        insRatio = feature_extractor.getInstRatio(code)
        ngram = filterNGrams(feature_extractor.getNgram(filePath,4),posNgrams)
        callsDump = filterCallsDump(feature_extractor.getCallsDump(code,posCalls))
        result.append([ngram,callsDump,insRatio,imports,tampered,packed])       
    return result

def collectFeaturesSingleFile(filePath, posNgrams, posCalls) -> list:
    result = []
    element = pe_parser.createObject(filePath)
    code = element.getCode()
    imports = element.getImports()
    tampered = element.getTampSections()
    packed = element.getPacked()
    insRatio = feature_extractor.getInstRatio(code)
    ngram = filterNGrams(feature_extractor.getNgram(filePath,4),posNgrams)
    callsDump = filterCallsDump(feature_extractor.getCallsDump(code,posCalls))
    result.append([ngram,callsDump,insRatio,imports,tampered,packed])
    return result

def collectBaseFeatures(filePath):
    result = []
    for file in os.listdir(filePath):
        print('Collecting values from file:',file)
        element = pe_parser.createObject(f"{filePath}\\{file}")
        code = element.getCode()
        imports = element.getImports()
        tampered = element.getTampSections()
        packed = element.getPacked()
        insRatio = feature_extractor.getInstRatio(code)
        result.append([insRatio,imports,tampered,packed])       
    return result

def transformToDataSet(folders,destFolder):
    listNG = []
    listCD = []
    listIR = []
    listIM = []
    listOH = []
    listVL = []
    
    topNgrams = list(map(int,pd.read_csv("Anti-malware-tool/posNgrams.csv",delimiter=";").columns.tolist()))
    topCalls = pd.read_csv("Anti-malware-tool/posCalls.csv",delimiter=";").columns.tolist()
    filesFlag = 0
    for filepath in folders:
        for file in os.listdir(filepath):
            print('Collecting values from file:',file)
            path = f"{filepath}\\{file}"
            element = pe_parser.createObject(path)
            code = element.getCode()
            imports = element.getImports()
            tampered = element.getTampSections()
            packed = element.getPacked()
            insRatio = feature_extractor.getInstRatio(code)
            ngram = filterNGrams(path,topNgrams)
            callsDump = filterCallsDump(code,topCalls)
            
            listNG.append(ngram)
            listCD.append(callsDump)
            listIR.append(insRatio)
            listIM.append(imports)
            listOH.append([int(tampered),int(packed)])
            if filesFlag:
                listVL.append([1])
            else:
                listVL.append([0])
        filesFlag = 1
    pd.DataFrame(listNG).to_csv(f"{destFolder}/ngram.csv",index=False,header=False)
    pd.DataFrame(listCD).to_csv(f"{destFolder}/calls.csv",index=False,header=False)
    pd.DataFrame(listIR).to_csv(f"{destFolder}/inst.csv",index=False,header=False)
    pd.DataFrame(listIM).to_csv(f"{destFolder}/imports.csv",index=False,header=False)
    pd.DataFrame(listOH).to_csv(f"{destFolder}/other.csv",index=False,header=False)
    pd.DataFrame(listVL).to_csv(f"{destFolder}/val.csv",index=False,header=False)
 
 
transformToDataSet([r"C:\Users\Martin\Desktop\negativeSamples",r"C:\Users\Martin\Desktop\pos_samples\Win32_EXE2021\train_data"],"train_data")  

