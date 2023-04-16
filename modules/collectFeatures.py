from modules import feature_extractor
from modules.pe_parser import createObject, Element_PE
import os
from ctypes import *
import pandas as pd

"""collectNGrams(filepath,ngramSize,ngramCount)
Collects ngram values from all files in the given directory and returns the ngramCount most common ngrams.
"""
def collectTopNGrams(filepath,ngramSize,ngramCount):
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Build the relative path to ngram_ext.so
    path = os.path.join(script_dir, "\\c_modules\\nsort.so")
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
        try:
            element = createObject(f"{filepath}\\{file}")
            callDump = feature_extractor.getCallsDump(element.getCode())
        except:
            continue
        if callDump == None:
            continue
        for x in callDump:
            if x in result:
                result[x] += 1
            else:
                result[x] = 1                
    return set([key for key, value in sorted(result.items(), key=lambda x: x[1], reverse=True)[:count]])
    
"""method
Methods collectNGrams and collectCallsDumps have to be used with positive and negative samples separately. Then 
collected features from positive samples will be removed from negative feature set.
"""


def filterNGrams(file,posNgrams):
    result = [0] * len(posNgrams)
    values = feature_extractor.getNgramC(file,4)
    intersection = set(posNgrams).intersection(set(values))
    for i in intersection:
        result[posNgrams.index(i)] = 1
    return result


def filterCallsDump(code,posCalls):
    result = [0] * len(posCalls)
    callDump = feature_extractor.getCallsDump(code)
    intersection = set(posCalls).intersection(set(callDump))
    for i in intersection:
        result[posCalls.index(i)] = 1
    return result

def collectFeaturesForNI(filePath, posNgrams) -> list:
    result = []
    element = createObject(filePath)
    imports = element.getImports()
    ngram = filterNGrams(filePath, posNgrams)
    result.append([pd.DataFrame(ngram).transpose(),
                   pd.DataFrame(imports).transpose()])
    return result, element.getHash()

def collectFeaturesForBI(filePath, posCalls) -> list:
    result = []
    element = createObject(filePath)
    code = element.getCode()
    imports = element.getImports()
    callsDump = filterCallsDump(code, posCalls)
    result.append([pd.DataFrame(callsDump).transpose(),
                   pd.DataFrame(imports).transpose()])
    return result, element.getHash()

def transformToDataSet(folders,destFolder):
    listNG = []
    listCDp = []
    listIR = []
    listIM = []
    listOH = []
    listVL = []
    counter = 0

    topNgrams = list(map(int,pd.read_csv("Anti-malware-tool/topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
    posCalls = pd.read_csv("topFeatures/posCalls.csv",delimiter=";").columns.tolist()
    filesFlag = 1
    for filepath in folders:
        for file in os.listdir(filepath):
            print(f"{counter/55702 * 100}%")
            print('Collecting values from file:',file)
            path = f"{filepath}\\{file}"
            try:
                element = createObject(path)
            except:
                print("Invalid NT header skipping file")
                continue
            code = element.getCode()
            imports = element.getImports()
            tampered = element.getTampSections()
            packed = element.getPacked()
            insRatio = feature_extractor.getInstRatio(code)
            ngram = filterNGrams(path,topNgrams)
            callsDumpP = filterCallsDump(code,posCalls)
            
            listNG.append(ngram)
            listCDp.append(callsDumpP)
            listIR.append(insRatio)
            listIM.append(imports)
            listOH.append([int(tampered),int(packed)])
            if filesFlag:
                listVL.append([1])
            else:
                listVL.append([0])
            counter += 1
        filesFlag = 1
    pd.DataFrame(listNG).to_csv(f"{destFolder}/ngram.csv",index=False,header=False)
    pd.DataFrame(listCDp).to_csv(f"{destFolder}/callsPos.csv",index=False,header=False)
    pd.DataFrame(listIR).to_csv(f"{destFolder}/inst.csv",index=False,header=False)
    pd.DataFrame(listIM).to_csv(f"{destFolder}/imports.csv",index=False,header=False)
    pd.DataFrame(listOH).to_csv(f"{destFolder}/other.csv",index=False,header=False)
    pd.DataFrame(listVL).to_csv(f"{destFolder}/val.csv",index=False,header=False)
 