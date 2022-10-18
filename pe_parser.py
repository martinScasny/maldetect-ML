import pefile

# PE CLASS ######################
def extractCode(bin):
  # TODO
  pass

def extractStrings(bin):
  # TODO
  pass

def extractImports(bin):
  # TODO
  pass
def calcEntropy(bin):
  # TODO
  pass

class Element_PE(bin):
  def __init__(self):
      self.code = extractCode(bin)
      self.strings = extractStrings(bin)
      self.imports = extractImports(bin)
      self.entropy = calcEntropy(bin)
    
  def getCode(self): return self.code
  def getStrings(self): return self.strings
  def getImports(self): return self.imports
  def getEntropy(self): return self.entropy
###############################


def packerCheck(entropy):
  # TODO
  # pestudio or smt else for packer detection
  pass

def createObject(filename) -> Element_PE:
  bin = open(filename, "rb")
  object = Element_PE(bin)
  
  return object
  