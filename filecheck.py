import os

filepath = r"C:\Users\Martin\Desktop\Samples\virusshare\VirusShare_00448"
bad_files = "bad_files.txt"
output_fd = open(bad_files,"w")
goodCounter = 0
for file in os.listdir(filepath):
    fd = open(f"{filepath}\\{file}","rb")
    magic = fd.read(2)
    if magic != b"MZ":
        output_fd.write(f"{filepath}\\{file}\n")
    else:
        goodCounter += 1
        
print(f"Good files: {goodCounter}")
output_fd.close()
