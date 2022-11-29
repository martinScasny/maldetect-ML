import feature_extractor
import os
import ctypes
import numpy as np

def collectNGrams(filepath,ngramSize,ngramCount):
    # values ngramy z aktualneho suboru, musia byt unikatne, tie prida a pripocita count, cize pole poli
    # nakoniec vyberie n najcastejsich
    # [ins][count]
    # sort by count
    # 
    py_values = list()
    arr = (ctypes.c_ushort * (pow(2,32)))(*py_values)
    
    mypath = filepath
    # collect all ngram values 
    for file in os.listdir(mypath):
        print('Collecting values from file:',file)
        values = feature_extractor.getNgram(f"{filepath}\\{file}",ngramSize)
        for x in values:
            arr[x] += 1
        print('Values were collected...')
    print("Sorting is happening ...")
    # replace with C func
    ntopValues = nsort(arr)
    sorted_arr = np_arr[np.argsort(np_arr[:,0],kind='heapsort')]
    # 
    print("DONE :)")
    result = sorted_arr.tolist()[-ngramCount:]
    return [result[x][1] for x in range(len(result))]
    
    
# arr = [[0,x] for x in range(10)]
# result = np.array(arr)
# print(arr)
# values = [np.random.randint(10) for x in range(10)]
# print(values)
# for x in values:
#     result[x][0] += 1
# print(result)
# sorted_index = result[np.argsort(result[:, 0],kind='heapsort')]

# # print(reversed(list(sorted_index[-3:]))[:,1])
# result = sorted_index.tolist()[-3:]
# print([result[x][1] for x in range(len(result))])

topNGrams = collectNGrams('C:\\Users\\Martin\\Desktop\\Samples',3,2000)
print(topNGrams)