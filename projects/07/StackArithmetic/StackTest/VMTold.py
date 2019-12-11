import sys


# line -> list
def parseLine(line):
  return line.split(' ')

# list -> line
def unparseList(list):
  return " ".join(list)

# parsed line (aka list) -> (format) [comment, hack inst, hack inst, ...]
# include commented VM line in front
def translateParsedLine(pl):
  id = pl[0]
  if id == 'push'or id == 'pop':
    return handlePushPop(pl)
  elif id in ['add', 'eq', 'lt', 'gt', 'neg', 'sub', 'or', 'not', 'and']:
    return handleArith(pl)

# parsed VM list -> parsed Hack list w/ comment head
# only handles constants now
def handlePushPop(list):
  comment = '{}'.format(unparseList(list))
  if list[1] == 'constant':
    return [comment]

def handleArith(list):
  print('hmm')
  return list

# VM line -> Hack line
def convertLine(VMline):
  VMline = VMline.strip()
  parsedLine = parseLine(VMline)
  return translateParsedLine(parsedLine)

# list of lists of Hack lines -> outfile string name -> txt file
def writeOutFileTo(lolohl, filename):
  openedOutFile = open(filename, 'w')
  print(lolohl)
  for list in lolohl:
    for line in list:
      openedOutFile.write(line)
      openedOutFile.write('\n')
  openedOutFile.close()
  return filename

def convert(file):
  filenameWOext = file.split('.')[0]
  outfilename = '{}.asm'.format(filenameWOext)

  opened = open(file, 'r')
  lines = opened.readlines()
  convertedLines = list(filter(None,list(map(convertLine, lines))))
  return writeOutFileTo(convertedLines, outfilename)

if __name__ == '__main__':
  # will need to handle both files and directories in future
  filename = sys.argv[-1]
  convert(filename)
