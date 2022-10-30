from fileinput import close
import pefile
import sys
import math
import re


def isSectionExecutable(section):
    characteristics = getattr(section, 'Characteristics')
    if characteristics & 0x00000020 > 0 or characteristics & 0x20000000 > 0:
        return True
    return False

def isPacked(section):
  set = section.get_data(ignore_padding=False)
  length = len(set)
  sum = [0]*256
  for x in set:
    sum[int(x)] += 1

  entropy = 0
  for x in sum:
    if x > 0:
      entropy +=  x/length * math.log(1/(x/length),2) 
  
  print("Entropia pre sekciu",section.Name,"je",entropy)
  return entropy > 7.2

def extractCode(pe):
  result = b""
  i = 0
  for section in pe.sections:
    if section.SizeOfRawData is not 0 and isSectionExecutable(section) and not isPacked(section):
      result += section.get_data(ignore_padding=False)
      i += 1
  print("I ma hodnotu ",i,sys.getsizeof(result))
  return result

def extractStrings(filename):
  result = []
  file = open(filename, 'rb')
  inbytes = file.read()
  s = []
  for x in inbytes:
    if x > 126: continue
    elif x > 32: s.append(chr(x))
    elif x is 0: s.append(" ")
  s = "".join(s)
  result.append(re.findall(r"(\d{1,3}\.){3}\d{1,3}", s))
  result.append(re.findall(r"/www|[a-zA-Z0-9]{6,}\.[a-zA-Z]{2,3}|http|https|:\/\//gm",s))
  result.append(re.findall(r"[a-zA-Z.:/]{7,}\s",s))
  # result.append(re.findall(r"([a-zA-Z0-9]\ ){5,}",s)) TODO 
  file.close()
  temp = result[0] + result[1] + result[2]
  result = temp
  return result


def extractImports(pe):
  res_imports = []
  for entry in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in entry.imports:
      res_imports.append(imp.name)
      
  for i in range(len(res_imports)):
    res_imports[i] = res_imports[i].decode()
    
  return res_imports
      
def calcEntropy(pe):
  # TODO
  pass

class Element_PE():
  def __init__(self,pe,filename):
    self.code = extractCode(pe)
    self.strings = extractStrings(filename)
    self.imports = extractImports(pe)

    
  def getCode(self): return self.code
  def getStrings(self): return self.strings
  def getImports(self): return self.imports
  def getEntropy(self): return self.entropy
###############################


def packerCheck(entropy):
  # TODO
  # pestudio or smt else for packer detection
  pass

def createObject(filename):
  pe = pefile.PE(filename)
  object = Element_PE(pe,filename)
  return object
  
peelement = createObject('sample31')
for x in peelement.getStrings():
  print(x)


