import sys

# Parser
class Parser:
  def __init__(self, filename):
    self.VMlines = list(filter(lambda x: (len(x) > 0), list(map(lambda x: (x.strip()), list(filter(lambda x: (x[0] != '/'), list(filter(None,open(filename, 'r').readlines()))))))))
    self.currentIndex = None
    self.currentCommand = None
    self.currentCommandType = None
    self.commandTypeDict = {'arithmetic' : 'C_ARITHMETIC', 'push' : 'C_PUSH', 'pop' : 'C_POP'}
    self.arithmetic = ['add', 'eq', 'lt', 'gt', 'neg', 'sub', 'or', 'not', 'and']


  def hasMoreCommands(self):
    if (len(self.VMlines) > 0 and self.currentIndex == None) or (len(self.VMlines) > self.currentIndex + 1):
      return True
    else:
      return False

  def advance(self):
    if self.hasMoreCommands():
      self.advanceIndex()
      self.currentCommand = self.VMlines[self.currentIndex].strip()

  def advanceIndex(self):
    if self.currentIndex == None and self.hasMoreCommands():
      self.currentIndex = 0
    elif self.hasMoreCommands():
      self.currentIndex += 1

  def commandType(self):
    if self.currentCommand != None:
      if self.arg0() in self.arithmetic:
        self.currentCommandType = self.commandTypeDict['arithmetic']
      else:
        self.currentCommandType = self.commandTypeDict[self.arg0()]
    return self.currentCommandType
  
  def arg0(self):
    if self.currentCommand != None:
      return self.currentCommand.split(' ')[0]

  def arg1(self):
    if self.currentCommand != None and self.currentCommand != 'C_RETURN':
      if self.currentCommandType == 'C_ARITHMETIC':
        return self.currentCommand.split(' ')[0]
      else:
        return self.currentCommand.split(' ')[1]

  def arg2(self):
    if self.currentCommand != None and self.currentCommandType in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
      return self.currentCommand.split(' ')[2]

class CodeWriter:
  def __init__(self, filename):
    self.openedoutfile = open(self.setFileName(filename), 'w')
    self.stack = MemorySegment(256, 2047)
    self.gotoVal1 = 0
    self.gotoVal2 = 1
    self.gotoValEnd = 2

  def setFileName(self,filename):
    print('VM translation has started')
    return '{}.asm'.format(filename.split('.')[0])

  def setNewGotoVals(self):
    self.gotoVal1 += 3
    self.gotoVal2 += 3
    self.gotoValEnd += 3

  def gotoLabel(self, gotoVal):
    return '(GOTO{})'.format(gotoVal)

  def gotoForAReg(self, gotoVal):
    return '@GOTO{}'.format(gotoVal)

  def callAppropriateWrite(self, parser):
    comment = '// {} \n'.format(parser.currentCommand)
    self.openedoutfile.write(comment)
    if parser.commandType() == 'C_ARITHMETIC':
      self.writeArithmetic(parser.arg1())
    if parser.commandType() == 'C_PUSH' or parser.commandType() == 'C_POP':
      self.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

  def writeArithmetic(self, command):
    self.writeASM(self.handleArithmetic(command))
    
  def handleArithmetic(self, command):
#['add', 'eq', 'lt', 'gt', 'neg', 'sub', 'or', 'not', 'and']
    list = []
    list.append('@SP')
    list.append('A=M-1')
    list.append('D=M')
    list.append('@SP')
    list.append('M=M-1')
    if command == 'add':
      list.append('@SP')
      list.append('A=M-1')
      list.append('D=D+M')
      list.append('M=D')
    elif command == 'eq':
      self.callEqLtGt(list, 'JEQ')
    elif command == 'lt':
      self.callEqLtGt(list, 'JLT')
    elif command == 'gt':
      self.callEqLtGt(list, 'JGT')
    elif command == 'neg':
      list.append('A=M')
      list.append('M=-D')
      list.append('@SP')
      list.append('M=M+1')
    elif command == 'sub':
      list.append('@SP')
      list.append('A=M-1')
      list.append('D=M-D')
      list.append('M=D')
    elif command == 'or':
      list.append('@SP')
      list.append('A=M-1')
      list.append('M=D|M')
    elif command == 'not':
      list.append('A=M')
      list.append('M=!M')
      list.append('@SP')
      list.append('M=M+1')     
    elif command == 'and':
      list.append('@SP')
      list.append('A=M-1')
      list.append('M=D&M')
    return list

  def callEqLtGt(self, list, jCommand):
    list = list
    self.setNewGotoVals()
    list.append('@SP')
    list.append('A=M-1')
    list.append('D=M-D')
    list.append(self.gotoForAReg(self.gotoVal1))
    list.append('D;{}'.format(jCommand)) 
    list.append('@SP')
    list.append('A=M-1')
    list.append('M=0')
    list.append(self.gotoForAReg(self.gotoValEnd))
    list.append('0;JMP')
    list.append(self.gotoLabel(self.gotoVal1))
    list.append('@SP')
    list.append('A=M-1')
    list.append('M=-1')
    list.append(self.gotoLabel(self.gotoValEnd))
    

  def writePushPop(self, command, segment, index):
    if command == 'C_PUSH':
      self.writeASM(self.handlePush(segment, index))
    elif command == 'C_POP':
      self.writeASM(self.handlePop(segment, index))

  def handlePopHelper(self, list, index):
    list.append('D=M')
    list.append('@{}'.format(index))
    list.append('D=D+A')
    list.append('@R15')
    list.append('M=D')  # R15 holds address where to store *sp val
    list.append('@SP')
    list.append('D=M-1')
    list.append('M=D')
    list.append('@SP')
    list.append('A=M')
    list.append('D=M')
    list.append('@R15')
    list.append('A=M')
    list.append('M=D')
    return list

  def handlePopHelperTemp(self, list, index):
    list.append('D=A')
    list.append('@{}'.format(index))
    list.append('D=D+A')
    list.append('@R15')
    list.append('M=D')  # R15 holds address where to store *sp val
    list.append('@SP')
    list.append('D=M-1')
    list.append('M=D')
    list.append('@SP')
    list.append('A=M')
    list.append('D=M')
    list.append('@R15')
    list.append('A=M')
    list.append('M=D')
    return list

  def handlePop(self, segment, index):
    list = []
    if segment == 'local':
      list.append('@LCL')
      list =  self.handlePopHelper(list, index)
    if segment == 'argument':
      list.append('@ARG')
      list = self.handlePopHelper(list, index)
    if segment == 'this':
      list.append('@THIS')
      list = self.handlePopHelper(list, index)
    if segment == 'that':
      list.append('@THAT')
      list =  self.handlePopHelper(list, index)
    if segment == 'temp':
      list.append('@R5')
      list =  self.handlePopHelperTemp(list, index)
    if segment == 'pointer':
      list.append('@SP')
      list.append('D=M-1')
      list.append('M=D')
      list.append('@SP')
      list.append('A=M')
      list.append('D=M')
      if index == '0':
        list.append('@THIS')
      if index == '1':
        list.append('@THAT')
      list.append('M=D')
    return list

  def handlePushHelper(self, list, index):
    list.append('D=M')
    list.append('@{}'.format(index))
    list.append('D=D+A')
    list.append('A=D')
    list.append('D=M')   # D = val to add to stack
    list.append('@R15')
    list.append('M=D')   #R15 = val to add to stack
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('D=M+1')
    list.append('M=D')
    return list

  def handlePushHelperTemp(self, list, index):
    list.append('D=A')
    list.append('@{}'.format(index))
    list.append('D=D+A')
    list.append('A=D')
    list.append('D=M')   # D = val to add to stack
    list.append('@R15')
    list.append('M=D')   #R15 = val to add to stack
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('D=M+1')
    list.append('M=D')
    return list


  def handlePush(self, segment, index):
    # need local, arg, this, that, temp
    list = []
    if segment == 'local':
      list.append('@LCL')
      list =  self.handlePushHelper(list, index)
    if segment == 'argument':
      list.append('@ARG')
      list =  self.handlePushHelper(list, index)
    if segment == 'this':
      list.append('@THIS')
      list =  self.handlePushHelper(list, index)
    if segment == 'that':
      list.append('@THAT')
      list =  self.handlePushHelper(list, index)
    if segment == 'temp':
      list.append('@R5')
      list =  self.handlePushHelperTemp(list, index)
    if segment == 'constant':
      list.append('@{}'.format(index))
      list.append('D=A')
      list.append('@SP')
      list.append('A=M')
      list.append('M=D')
      list.append('@SP')
      list.append('M=M+1')
    if segment == 'pointer':
      if index == '0':
        list.append('@THIS')
      if index == '1':
        list.append('@THAT')
      list.append('D=M')
      list.append('@SP')
      list.append('A=M')
      list.append('M=D')
      list.append('@SP')
      list.append('D=M+1')
      list.append('M=D')
    return list 
      
  # list of ASM -> write each to outfile
  def writeASM(self, loASM):
    for ASMline in loASM:
      self.openedoutfile.write(ASMline)
      self.openedoutfile.write('\n')

  def initPointers(self):
    #will need to add more later
    list = []
    list.append('@256')
    list.append('D=A')
    list.append('@SP')
    list.append('M=D')

    self.writeASM(list)


  def close(self):
    self.openedoutfile.close()

class MemorySegment:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.size = end - start + 1
    self.sp = start

if __name__ == '__main__':
  # will need to handle both files and directories in future
  # when handling a directory, make diff parsers for each file within, but still only use one CodeWriter
  filename = sys.argv[-1]
  
  p1 = Parser(filename)
  c1 = CodeWriter(filename)
  c1.initPointers()
  while p1.hasMoreCommands():
    p1.advance()
    c1.callAppropriateWrite(p1)
  c1.close()
