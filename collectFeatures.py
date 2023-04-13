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
        try:
            element = pe_parser.createObject(f"{filepath}\\{file}")
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
    element = pe_parser.createObject(filePath)
    code = element.getCode()
    imports = element.getImports()
    ngram = filterNGrams(filePath, posNgrams)
    result.append([pd.DataFrame(ngram).transpose(),
                   pd.DataFrame(imports).transpose()])
    return result, element.getHash()

def collectFeaturesForBI(filePath, posCalls) -> list:
    result = []
    element = pe_parser.createObject(filePath)
    code = element.getCode()
    imports = element.getImports()
    callsDump = filterCallsDump(code, posCalls)
    result.append([pd.DataFrame(callsDump).transpose(),
                   pd.DataFrame(imports).transpose()])
    return result, element.getHash()

def transformToDataSet(folders,destFolder):
    # listNG = []
    listCDp = []
    listIR = []
    listIM = []
    listOH = []
    listVL = []
    counter = 0

    # topNgrams = list(map(int,pd.read_csv("Anti-malware-tool/topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
    posCalls = pd.read_csv("Anti-malware-tool/topFeatures/posCalls.csv",delimiter=";").columns.tolist()
    filesFlag = 1
    for filepath in folders:
        for file in os.listdir(filepath):
            print(f"{counter/55702 * 100}%")
            print('Collecting values from file:',file)
            path = f"{filepath}\\{file}"
            try:
                element = pe_parser.createObject(path)
            except:
                print("Invalid NT header skipping file")
                continue
            code = element.getCode()
            imports = element.getImports()
            tampered = element.getTampSections()
            packed = element.getPacked()
            insRatio = feature_extractor.getInstRatio(code)
            # ngram = filterNGrams(path,topNgrams)
            callsDumpP = filterCallsDump(code,posCalls)
            
            # listNG.append(ngram)
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
    # pd.DataFrame(listNG).to_csv(f"{destFolder}/ngram.csv",index=False,header=False)
    pd.DataFrame(listCDp).to_csv(f"{destFolder}/callsPos.csv",index=False,header=False)
    pd.DataFrame(listIR).to_csv(f"{destFolder}/inst.csv",index=False,header=False)
    pd.DataFrame(listIM).to_csv(f"{destFolder}/imports.csv",index=False,header=False)
    pd.DataFrame(listOH).to_csv(f"{destFolder}/other.csv",index=False,header=False)
    pd.DataFrame(listVL).to_csv(f"{destFolder}/val.csv",index=False,header=False)
 

# pathToPositiveSamples = r'C:\Users\Martin\Desktop\Samples\Positives'
# pathToNegativeSamples = r'C:\Users\Martin\Desktop\Samples\Negatives'
# transformToDataSet([pathToNegativeSamples,pathToPositiveSamples],"train_data4")

# posNgrams = collectTopNGrams(pathToPositiveSamples,4,10000) - collectTopNGrams(pathToNegativeSamples,4,10000)
# posCalls = collectTopCallsDump(pathToPositiveSamples, 2000)
# negCalls = collectTopCallsDump(pathToNegativeSamples, 2000)
# print(len(posCalls),len(negCalls))
# calls = posCalls - negCalls
# print(len(calls))

# output_file = open(r'posCallsNew.csv','w')
# result = ""
# for item in posCalls:
#     result += str(item)
#     result += ";"
# result = result[:-1]
# output_file.write(result)
# output_file.close()

# output_file = open(r'negCalls.csv','w')
# result = ""
# for item in negCalls:
#     result += str(item)
#     result += ";"
# result = result[:-1]
# output_file.write(result)
# output_file.close()

# output_file = open(r'uniCalls.csv','w')
# result = ""
# for item in calls:
#     result += str(item)
#     result += ";"
# result = result[:-1]
# output_file.write(result)
# output_file.close()
