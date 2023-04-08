import os
import time
import feature_extractor
import collectFeatures
import pandas as pd


# load before parsing file to save time
topNgrams = list(map(int,pd.read_csv("topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
topCalls = pd.read_csv("topFeatures/posCalls.csv",delimiter=";").columns.tolist()
start_time = time.perf_counter()
features = collectFeatures.collectFeaturesFromFile("Anti-malware-tool/sample5mb", topNgrams, topCalls)
print("--- %s seconds ---" % (time.perf_counter() - start_time))

# filepath = r"C:\Users\Martin\Desktop\Samples\virusshare\VirusShare_00448"
# bad_files = "bad_files.txt"
# output_fd = open(bad_files,"w")
# goodCounter = 0
# for file in os.listdir(filepath):
#     fd = open(f"{filepath}\\{file}","rb")
#     magic = fd.read(2)
#     if magic != b"MZ":
#         output_fd.write(f"{filepath}\\{file}\n")
#     else:
#         goodCounter += 1
        
# print(f"Good files: {goodCounter}")
# output_fd.close()
