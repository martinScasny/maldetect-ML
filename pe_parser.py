from fileinput import close
from capstone import *
import pefile
import sys
import math
import re
import hashlib

list_of_imports = ['LoadLibrary',
                   'ShellExecute',
                   'GetProcAddress',
                   'GetVersionEx',
                   'GetModuleHandle',
                   'OpenProcess',
                   'GetWindowsDirectory',
                   'WriteFile',
                   'ReadFile',
                   'GetFileSize',
                   'CreateFile',
                   'DeleteFile',
                   'CreateProcess',
                   'GetCurrentProcess',
                   'RegOpenKeyEx',
                   'GetStartupInfo',
                   'CreateService',
                   'CopyFile',
                   'GetModuleFileName',
                   'IsbadReadPtr'
                   'SetFilePointer',
                   'VirtualAlloc',
                   'AdjustTokenPrivileges',
                   'CloseHandle',
                   'GetTempPath',
                   'IsBadWritePtr',
                   'UrlDownloadToFile',
                   'WinExec',
                   'GetCommandLine',
                   'StartService',
                   'VirtualProtect',
                   'WriteProcessMemory',
                   'HeapCreate',
                   'MapViewOfFile',
                   'CreateRemoteThread',
                   'CreateToolhelp32Snapshot',
                   'GetProcessHeap',
                   'Sleep',
                   'ZwCreateFile',
                   'RtlCreateHeap',
                   'ZwUnmapViewOfSection',
                   'ZwCreateProcess',
                   'ZwCreateThread',
                   'ZwcreateUserProcess',
                   'RtlAddVectoredExceptionHandler',
                   'ZwAllocateVirtualMemory',
                   'LdrHotPatchRoutine',
                   'ZwWriteVirtualMemory',
                   'ZwMapViewOfSection',
                   'ZwCreateSection',
                   'ZwCreateProcessEx',
                   'LdrLoadDll',
                   'ZwProtectVirtualMemory',
                   ]

#function that will iterate through entries and check wheter entry is in list_of_imports
def filterImports(entries):
    result = [0]*len(list_of_imports)
    for entry in entries:
      if entry != None:
        for i in range(len(list_of_imports)):
            if list_of_imports[i] in entry:
                result[i] = 1
    return result

# BUF_SIZE is totally arbitrary, change for your app!
def makeHash(filename):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    return [md5.hexdigest(),sha1.hexdigest()]
  
def isSectionExecutable(section):
    characteristics = getattr(section, 'Characteristics')
    if characteristics & 0x00000020 > 0 or characteristics & 0x20000000 > 0:
        return True
    return False

def isSectionPacked(section):
  set = section.get_data(ignore_padding=False)
  length = len(set)
  sum = [0]*256
  for x in set:
    sum[int(x)] += 1

  entropy = 0
  for x in sum:
    if x > 0:
      entropy +=  x/length * math.log(1/(x/length),2)  
  return entropy > 7.2

def isBinPacked(pe):
  for section in pe.sections:
    if isSectionExecutable(section) and isSectionPacked(section):
      return True
  return False
  
def extractCode(pe):
  code = b""
  i = 0
  result = []
  for section in pe.sections:
    if section.SizeOfRawData != 0 and isSectionExecutable(section) and not isSectionPacked(section):
      code += section.get_data(ignore_padding=False)
      i += 1
  # capstone disassembly 
  md = Cs(CS_ARCH_X86, CS_MODE_64)
  for i in md.disasm(code, 0x1000):
      result.append([i.mnemonic, i.bytes])

  return result


def extractStrings(filename):
  print("Extracting strings...")
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

  """_tamperedSections
  This method compares names of each section with the list of known names.
  """
def tamperedSections(pe) -> bool: 
  knownSections = ['.text', '.data', '.rdata', '.idata', '.edata', '.rsrc', '.reloc']
  # cut trailing zeros from binary data b'.text\x00\x00\x00', that is stored in section.Name
  for section in pe.sections:
    try:
      if section.Name.decode().split('\x00')[0] not in knownSections:
        return True
    except:
      return False
  return False



def extractImports(pe):
  res_imports = []
  if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
      for imp in entry.imports:
        res_imports.append(imp.name)
        
    for i in range(len(res_imports)):
      if res_imports[i] is not None:
        res_imports[i] = res_imports[i].decode()
  
  return filterImports(res_imports)

##### CLASS #########################
class Element_PE():
  def __init__(self,pe,filename):
    self.__code = extractCode(pe)
    self.__filename = filename
    self.__imports = extractImports(pe)
    self.__hash = makeHash(filename)
    self.__packed = isBinPacked(pe)
    self.__tamperedSections = tamperedSections(pe)
    
  def getCode(self): return self.__code
  def getStrings(self): return extractStrings(self.__filename)
  def getImports(self): return self.__imports
  def getHash(self): return self.__hash
  def getPacked(self): return self.__packed
  def getTampSections(self): return self.__tamperedSections
###############################


def createObject(filename):
  pe = pefile.PE(filename)
  object = Element_PE(pe,filename)
  return object
