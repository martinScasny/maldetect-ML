import feature_extractor
import os
from ctypes import *
import numpy as np

def collectNGrams(filepath,ngramSize,ngramCount):
    # values ngramy z aktualneho suboru, musia byt unikatne, tie prida a pripocita count, cize pole poli
    # nakoniec vyberie n najcastejsich
    # [ins][count]
    # sort by count
    # 
    path = r'C:\Users\Martin\Desktop\Anti-malware-tool\Anti-malware-tool\nsort.so'
    libObject = CDLL(path)
    nsort = libObject.findNTopValues
    nsort.argtypes = [c_int, POINTER(c_uint16), c_uint16]
    nsort.restype = POINTER(POINTER(c_uint16))
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
        result.append(ntopValues.content[x])
    
    return result
    
    

topNGrams = collectNGrams('C:\\Users\\Martin\\Desktop\\Samples',4,2000)
print(topNGrams)

# arr = (c_uint16 * (pow(255,4)))()
# arrPtr = pointer(arr)
# arrPtr.contents[0] = 23
# arrPtr.contents[1] = 54
# print(arrPtr.contents[0],arrPtr.contents[1])