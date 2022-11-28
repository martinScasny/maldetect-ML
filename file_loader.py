import os

def handler(filepath):
  savedSet = set()
  mypath = filepath

  nameSet = set()
  for file in os.listdir(mypath):
      fullpath = os.path.join(mypath, file)
      if os.path.isfile(fullpath):
          nameSet.add(file)
  
  newSet = nameSet - savedSet
  savedSet = newSet
  
  print(savedSet)

# multi threaded application later
# for now TODO - one at a time, infinite loop
# send logs to file
handler()