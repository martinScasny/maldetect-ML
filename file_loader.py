import os

def handler():
  savedSet = set()
  mypath = "."

  nameSet = set()
  for file in os.listdir(mypath):
      fullpath = os.path.join(mypath, file)
      if os.path.isfile(fullpath):
          nameSet.add(file)

  newSet = nameSet - savedSet
  savedSet = newSet

# multi threaded application later
# for now TODO - one at a time, infinite loop
# send logs to file