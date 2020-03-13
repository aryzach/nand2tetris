import sys
import os
from os import listdir
from os.path import isfile, join
import glob 

# Parser
class Parser:
  def __init__(self, filename):
    self.VMlines = list(filter(lambda x: (len(x) > 0), list(map(lambda x: (x.strip()), list(filter(lambda x: (x[0] != '/'), list(filter(None,open(filename, 'r').readlines()))))))))
    self.currentIndex = None
    self.currentCommand = None
    self.currentCommandType = None
    self.commandTypeDict = {'arithmetic' : 'C_ARITHMETIC', 'push' : 'C_PUSH', 'pop' : 'C_POP', 'label' : 'C_LABEL', 'goto' : 'C_GOTO', 'if-goto' : 'C_IF', 'function' : 'C_FUNCTION', 'return' : 'C_RETURN', 'call' : 'C_CALL'}
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
    self.filename = ''
    self.currentFunction = None
    self.callReturnInstance = 0

  def setFileName(self,filename):
    print('VM translation has started')
    self.filename = filename.split('.')[0]
    return '{}.asm'.format(self.filename)

  def setNewGotoVals(self):
    self.gotoVal1 += 3
    self.gotoVal2 += 3
    self.gotoValEnd += 3

  def gotoLabel(self, gotoVal):
    return '(GOTO{})'.format(gotoVal)

  def gotoForAReg(self, gotoVal):
    return '@GOTO{}'.format(gotoVal)

  def callAppropriateWrite(self, parser, fn):
    comment = '// {} \n'.format(parser.currentCommand)
    self.openedoutfile.write(comment)
    if parser.commandType() == 'C_ARITHMETIC':
      self.writeArithmetic(parser.arg1())
    if parser.commandType() == 'C_PUSH' or parser.commandType() == 'C_POP':
      self.writePushPop(parser.commandType(), parser.arg1(), parser.arg2(), fn)
    if parser.commandType() == 'C_LABEL':
      self.writeLabel(parser.arg1())
    if parser.commandType() == 'C_GOTO':
      self.writeGoto(parser.arg1())
    if parser.commandType() == 'C_IF':
      self.writeIf(parser.arg1())
    if parser.commandType() == 'C_CALL':
      self.writeCall(parser.arg1(), parser.arg2())
    if parser.commandType() == 'C_RETURN':
      self.writeReturn()
    if parser.commandType() == 'C_FUNCTION':
      self.currentFunction = parser.arg1()
      self.writeFunction(parser.arg1(), parser.arg2())

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
    

  def writePushPop(self, command, segment, index, fn):
    if command == 'C_PUSH':
      self.writeASM(self.handlePush(segment, index, fn))
    elif command == 'C_POP':
      self.writeASM(self.handlePop(segment, index, fn))

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

  def handlePop(self, segment, index, fn):
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
    if segment == 'static':
      list.append('@SP')
      list.append('D=M-1')
      list.append('M=D')
      list.append('@SP')
      list.append('A=M')
      list.append('D=M')
      list.append('@{}.{}'.format(fn, index))
      print(fn)
      print('@{}.{}'.format(fn, index))
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


  def handlePush(self, segment, index, fn):
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
    if segment == 'static':
      list.append('@{}.{}'.format(fn, index))
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


  def writeInit(self):
    self.writeASM(self.handleInit())

  def handleInit(self):
    list = []
    list.append('@256')
    list.append('D=A')
    list.append('@SP')
    list.append('M=D')
    list = list + self.handleCall('Sys.init', '0')
    return list

  def writeLabel(self, label):
    self.writeASM(self.handleLabel(label))

  def handleLabel(self, label):
    list = []
#    if self.currentFunction == None:
#      list.append('({})'.format(label))
#    else:
#      list.append('({}${})'.format(self.currentFunction,label))
    list.append('({})'.format(label))
    return list
 
  def writeGoto(self, label):
    self.writeASM(self.handleGoto(label))

  def handleGoto(self, label):
    list = []
#    if self.currentFunction == None:
#      list.append('@{}'.format(label))
#    else:
#      list.append('@{}${}'.format(self.currentFunction,label))
    list.append('@{}'.format(label))
    list.append('0;JMP')
    return list

  def writeIf(self, label):
    self.writeASM(self.handleIf(label))

  def handleIf(self, label):
    list = []
    list.append('@SP')
    list.append('M=M-1')
    list.append('@SP')
    list.append('A=M')
    list.append('D=M')
#    if self.currentFunction == None:
#      list.append('@{}'.format(label))
#    else:
#      list.append('@{}${}'.format(self.currentFunction,label))
    list.append('@{}'.format(label))
    list.append('D;JNE')
    return list

  def writeCall(self, functionName, numArgs):
    self.writeASM(self.handleCall(functionName, numArgs))

  def handleCall(self, fn, na):
    self.callReturnInstance += 1
    list = []
    list.append('// push return-address')
    list.append('@return-{}-{}-{}'.format(fn, na, self.callReturnInstance))
    list.append('D=A')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('M=M+1')
    list.append('// push LCL')
    list.append('@LCL')
    list.append('D=M')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('M=M+1')
    list.append('// push ARG')
    list.append('@ARG')
    list.append('D=M')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('M=M+1')
    list.append('// push THIS')
    list.append('@THIS')
    list.append('D=M')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('M=M+1')
    list.append('// push THAT')
    list.append('@THAT')
    list.append('D=M')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('M=M+1')
    list.append('// ARG = SP-n-5')
    list.append('@{}'.format(na))
    list.append('D=A')
    list.append('@5')
    list.append('D=D+A')
    list.append('@SP')
    list.append('D=M-D')
    list.append('@ARG')
    list.append('M=D')
    list.append('// LCL = SP')
    list.append('@SP')
    list.append('D=M')
    list.append('@LCL')
    list.append('M=D')
    list.append('// goto f')
    list = list + self.handleGoto(fn)                #possible bug
    list.append('// (return-address)')
    list.append('(return-{}-{}-{})'.format(fn, na, self.callReturnInstance))
    return list

  def writeReturn(self):
    self.writeASM(self.handleReturn())

  def handleReturn(self):
    list = []
    list.append('// frame = LCL')
    list.append('@LCL')
    list.append('D=M')
    list.append('@FRAME')    # or should I go straight to temp?
    list.append('M=D')
    list.append('// ret = *(frame-5)')
    list.append('@FRAME')
    list.append('D=M')
    list.append('@5')
    list.append('D=D-A')
    list.append('A=D')
    list.append('D=M')
    list.append('@RET')
    list.append('M=D')
    list.append('// *arg = pop()')
    list = list + self.handlePop('argument', '0', '')  # possibly a bug
    list.append('// sp = arg+1')
    list.append('@ARG')
    list.append('D=M+1')
    list.append('@SP')
    list.append('M=D')
    list.append('// that = *(frame-1)')
    list.append('@FRAME')
    list.append('A=M-1')
    list.append('D=M')
    list.append('@THAT')
    list.append('M=D')
    list.append('// this = *(frame-2)')
    list.append('@2')
    list.append('D=A')
    list.append('@FRAME')
    list.append('A=M-D')
    list.append('D=M')
    list.append('@THIS')
    list.append('M=D')
    list.append('// arg = *(frame-3)')
    list.append('@3')
    list.append('D=A')
    list.append('@FRAME')
    list.append('A=M-D')
    list.append('D=M')
    list.append('@ARG')
    list.append('M=D')
    list.append('// lcl = *(frame-4)')
    list.append('@4')
    list.append('D=A')
    list.append('@FRAME')
    list.append('A=M-D')
    list.append('D=M')
    list.append('@LCL')
    list.append('M=D')
    list.append('// goto ret')
    list.append('@RET')
    list.append('A=M')
    list.append('0;JMP')    
    return list

  def writeFunction(self, functionName, numLocals):
    self.writeASM(self.handleFunction(functionName, numLocals))

  def handleFunction(self, fn, nl):
    list = []
    list.append('({})'.format(fn))
    list.append('@{}'.format(nl))
    list.append('D=A')
    list.append('@R14')
    list.append('M=D')
    list.append('({}$AddMoreLocVars)'.format(fn))  #might be buggy for same reason below
    list.append('@R14')
    list.append('D=M')
    list.append('@{}$NoMoreLocVars'.format(fn))     #might be buggy later if multiple functions are on stack 
    list.append('D;JEQ')
    list.append('@0')
    list.append('D=A')
    list.append('@SP')
    list.append('A=M')
    list.append('M=D')
    list.append('@SP')
    list.append('D=M+1')
    list.append('M=D')
    list.append('@R14')
    list.append('D=M-1')
    list.append('M=D')
    list.append('@{}$AddMoreLocVars'.format(fn))
    list.append('0;JMP')
    list.append('({}$NoMoreLocVars)'.format(fn))
    return list

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
  path = sys.argv[-1].split('/')[0]
  if os.path.isdir(path):
    cwd = os.getcwd()  
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]      
    onlyVMfiles = list(filter(lambda x: x[-3:] == '.vm', onlyfiles))
    onlyVMfiles2 = list(map(lambda x : '{}/{}'.format(path,x), onlyVMfiles))
    c1 = CodeWriter(path)
    c1.writeInit()
    for VMfile in onlyVMfiles2:
      fnWOext = VMfile.split('.')[0].split('/')[1]
      currentParser = Parser(VMfile)
      while currentParser.hasMoreCommands():
        currentParser.advance()
        c1.callAppropriateWrite(currentParser, fnWOext)
    c1.close()      
# below might be a bug now bc I added filename (to use in static)  
  elif os.path.isfile(path):  
    p1 = Parser(path)
    c1 = CodeWriter(path)
    # c1.writeInit()            #should I call this for files? or maybe just poiter init without sys init
    while p1.hasMoreCommands():
      p1.advance()
      c1.callAppropriateWrite(p1)
    c1.close()
