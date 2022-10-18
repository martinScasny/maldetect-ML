#imports
import os
import re

def findPE(filename):
  with open(os.path.join(os.getcwd(), filename), 'rb') as f:
  # TODO ideally in C using mmap and return pointer to address when PE file starts
    print()
  
if __name__ == "__main__":
# i ... iterator
  i = 0
# list all files in the directory
  for filename in os.listdir(os.getcwd()):
    curr_pe = b""
     # open in readonly mode
    curr_pe = findPE(filename)
    
    # create result PE file
    with open(f"sample{i}.bin", 'wb') as res:
      res.write(curr_pe,"wb")    
    i += 1
         