#imports
import os
import re

def findPE(filename):
  magic = [b'\x34',b'\x44',b'\x35',b'\x41']
  match = 0
  success = 0
  result = b''
  numofBytes = 1
  with open(os.path.join("C:\\Users\\Martin\\Desktop\\VirusShare_00341", filename), 'rb') as f:
    try:
      byte = f.read(numofBytes)
    except:
      byte = 'X'
    while byte:
      if not success:
        if byte == magic[match]:
          match += 1
          if match == 4:
            success = 1
            numofBytes = 2
            result += b'\x4d\x5a'
        else:
          match = 0
      else:
        try:
          listbyte = [hex(x) for x in list(byte)] 
        except:
          break
        if listbyte[0] == '0x22':
          break
        result += bytes.fromhex(byte.decode('ascii'))
      try:
        byte = f.read(numofBytes)
      except:
        pass
    return result
  
if __name__ == "__main__":
# i ... iterator
  i = 0
  j = 0
# list all files in the directory
  for filename in os.listdir("C:\\Users\\Martin\\Desktop\\VirusShare_00341"):
    print(i, filename)
    curr_pe = b""
     # open in readonly mode
    curr_pe = findPE(filename)
    
    # create result PE file
    if curr_pe is not b'':
      with open(f"C:\\Users\\Martin\\Desktop\\Samples\\sample{j}.bin", 'wb') as res:
        print(f"Found PE file number {j}, writing file")
        res.write(curr_pe)    
        j += 1
    i += 1
      # if i == 10:
      #   break