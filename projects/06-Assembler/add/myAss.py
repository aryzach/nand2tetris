cDict = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000'}
dDict = {

#full file to each line in array
def fullToLine(opened_file):
  lines = []
  with open(opened_file) as fp:
   for cnt, line in enumerate(fp):
     lines.append(line)
  return lines

def convertOneLine(line):
  if line[0] == '@':
    return convertA(line)
  elif line[0] in 'DMA':
    return convertC(line)
  else:
    return ''

def convertA(line):
  ll = len(line)
  return decToBin(line[1..ll])

def convertC(line):
  spl = line.split('=')
  spl2 = [spl[0]] + spl[1].split(';')
  print(spl2)
  if '=' in line and ';' in line:
    compV = spl2[1]
    destV = spl2[0]
    jumpV = spl2[2][0..(len(jumpV)-2)]
  elif '=' in line:
    compV = spl2[1][0..(len(compV)-2)]
    destV = spl2[0]
  elif ';' in line:
    compV = spl2[0]
    jumpV = spl2[1][0..(len(jumpV)-2)]
  return '111' + doC(compV) + doD(destV) + doJ(jumpV)

def doC(comp):
  if comp in cDict.keys():
    return cDict[comp]
  else:
    return 'errorComp'

def doD(dest):
  if dest in dDict.keys():
    return dDict[dest]
  else:
    return 'errorDest'
def doJ(jump):
  return jDict[jump]



if __name__ == '__main__':
  lines=fullToLine('/Users/Zach/Desktop/nand2tetris/projects/06/add/test.txt')
  fin = []
  for line in lines:
    fin.append(convertOneLine(line))
  print(fin)

g=open('path/to/file.txt', 'r')

g.close()

filepath = 'Iliad.txt'
with open(filepath) as fp:
   for cnt, line in enumerate(fp):
       print("Line {}: {}".format(cnt, line))


filepath = 'Iliad.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       cnt += 1
