import sys
import os
from os import listdir
from os.path import isfile, join
import glob
import re

SYMBOLS = ';{}&]-/=~'
REST_SYMBOLS = ',|().[<>+*'
KEYWORDS = ['class','method','function','constructor','int','boolean','char','void','var','static','field','let','do','if','else','while','return','true','false','null','this']
KEYWORD = 'keyword'
SYMBOL = 'symbol'
IDENTIFIER = 'identifier'
INT_CONST = 'integerConstant'
STRING_CONST = 'stringConstant'
CLASS = 'class'
METHOD = 'method'
FUNCTION = 'function'
CONSTRUCTOR = 'constructor'
INT = 'int'
BOOLEAN = 'boolean'
CHAR = 'char'
VOID = 'void'
VAR = 'var'
STATIC = 'static'
FIELD = 'field'
LET = 'let'
DO = 'do'
IF = 'if'
ELSE = 'else'
WHILE = 'while'
RETURN = 'return'
TRUE = 'true'
FALSE = 'false'
NULL = 'null'
THIS = 'this'

LOCAL = 'local'
ARG = 'argument'
class Tokenizer:
	def __init__(self, infile):
		self.allTokens = []
		self.currentToken = None
		self.origTokens = None
		self.infile = infile
		self.infileName = infile.split('.')[0]
		self.separate(infile)
		self.tokenIndex = 0
		self.outfile = self.openedOut()
		self.currentMarkedUpToken = None

	def openedOut(self):
		return open('{}Tmine.xml'.format(self.infileName), 'w')

	def separate(self,infile):
		# split by lines, comments, strings, spaces, then symbols
		noComments = self.removeComments(infile)
	
		noCommentSplitStrings = self.splitStrings(noComments)

		tokensDraft = []
		for phrase in noCommentSplitStrings:
			if phrase[0] != '"':
				tokensDraft += phrase.split()
			else:
				tokensDraft.append(phrase)

		self.allTokens = []
		for line in tokensDraft:
			self.allTokens += self.breakLineOnAllSymbols(line)	
		
		self.allTokens = list(filter(lambda x : len(x)>0, self.allTokens)) 

	def splitStrings(self, lophrases):
		splitList = []
		for phrase in lophrases:
			splitPhrase = phrase.split('"')
			if phrase[0] == '"':
				for i in range(0,len(splitPhrase),2):
					splitPhrase[i] = '"' + splitPhrase[i] + '"'
			else:
				for i in range(1,len(splitPhrase),2):
					splitPhrase[i] = '"' + splitPhrase[i] + '"'
			splitList += splitPhrase
		return splitList

	def removeComments(self, infile):
		# normal, inline, block, api
		withInlineComments = list(filter(lambda x : (x[0:2] != '//'),open(infile, 'r').readlines()))
		woInlineComments = []
		for line in withInlineComments:
			lineSplitInline = list(filter(lambda x : (len(x) > 0),line.split('//', 1)))
			woInlineComments.append(lineSplitInline[0].strip())
		woInlineComments = list(filter(lambda x : (len(x) > 0), woInlineComments))
		noComments = self.removeBlockComments(woInlineComments)
		return noComments

	def removeBlockComments(self, list):
		include = True
		noComments = []
		for line in list:
			if (line[0:3] == '/**') and (line[(-2):] == '*/'):
				continue
			if (line[0:3] == '/**') and (include == True):
				include = False
				continue
			elif line[(-2):] == '*/':
				include = True
				continue
			else:
				if include == True:
					noComments.append(line)
		return noComments

	def breakLineOnAllSymbols(self, line):
		if len(line) == 1:
			return [line]
		for letter in line:
			if letter in SYMBOLS or letter in REST_SYMBOLS:
				ls = line.split(letter, 1)
				return [ls[0], letter] + self.breakLineOnAllSymbols(ls[1])
		return [line]

	def hasMoreTokens(self):
		if len(self.allTokens) > self.tokenIndex:
			return True
		else:
			return False

	def advance(self):
		#get next token and make it the current token
		if self.hasMoreTokens():
			self.currentToken = self.allTokens[self.tokenIndex]
			self.tokenIndex += 1

	def tokenType(self):
		if self.currentToken in KEYWORDS:
			return KEYWORD
		if (len(self.currentToken)> 2) and (self.currentToken[0] == '"' and self.currentToken[-1] == '"'):
			return STRING_CONST
		if self.currentToken in SYMBOLS or self.currentToken in REST_SYMBOLS:
			return SYMBOL
		if self.isNum():
			return INT_CONST
		if self.isIdentifier():
			return IDENTIFIER

	def isIdentifier(self):
		if self.currentToken[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
			for letter in self.currentToken:
				if letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890':
					continue
				else:
					return False
			return True
		return False

	def isNum(self):
		total = 0
		for digit in self.currentToken:
			if digit in '1234567890':
				total += 1
		if total == len(self.currentToken):
			return True
		else:
			return False

	def keyWord(self):
		return self.currentToken

	def symbol(self):
		if self.currentToken == '<':
			return '&lt;'
		elif self.currentToken == '>':
			return '&gt;'
		elif self.currentToken == '&':
			return '&amp;'
		else:
			return self.currentToken

	def identifier(self):
		return self.currentToken

	def intVal(self):
		return int(self.currentToken) 

	def stringVal(self):
		return self.currentToken[1:-1]

	def currentTokenVal(self):
		if self.tokenType() == KEYWORD:
			return self.keyWord()
		elif self.tokenType() == STRING_CONST:
			return self.stringVal()
		elif self.tokenType() == SYMBOL:
			return self.symbol()
		elif self.tokenType() == INT_CONST:
			return self.intVal()
		elif self.tokenType() == IDENTIFIER:
			return self.identifier()

	def close(self):
		return None
		#close file

	def createMarkupToken(self):
		return '<{}> {} </{}>'.format(self.tokenType(),self.currentTokenVal(),self.tokenType())		

	def writeMarkupToken(self):
		self.outfile.write(self.createMarkupToken())
		self.outfile.write('\n')

	def writeExplicit(self, explicit):
		self.outfile.write(explicit)
		self.outfile.write('\n')

def mainProcess(filepath):
	ct = Tokenizer(filepath)
#	ct.writeExplicit('<tokens>')
	ce = CompilationEngine(ct,filepath)
#	print(ct.allTokens)
#	while ct.hasMoreTokens():
#		ct.advance()
#		ct.writeMarkupToken()
#	ct.writeExplicit('</tokens>')
	if ct.hasMoreTokens():
		ct.advance()
		ce.decide()
	ct.close()

class STentry:
	def __init__(self, name, jackType, kind, index):
		self.name = name
		self.jackType = jackType
		self.kind = kind
		self.index = index

class SymbolTable:
	def __init__(self):
		self.classScope = []
		self.subroutineScope = []

	def startSubroutine(self):
		self.subroutineScope = []

	def define(self, name, jackType, kind):
		if self.varCount(kind) == None:
			index = 0
		else:
			index = self.varCount(kind) + 1
		if kind == STATIC or kind == FIELD:
			self.classScope.append(STentry(name, jackType, kind, index))
		elif kind == VAR or kind == ARG:
			self.subroutineScope.append(STentry(name, jackType, kind, index))

	def varCount(self, kind):
		#returns int
		kindListIndex = []
		if kind == STATIC or kind == FIELD:
			for entry in self.classScope:
				if entry.kind == kind:
					kindListIndex.append(entry.index)
		elif kind == VAR or kind == ARG:
			for entry in self.subroutineScope:
				if entry.kind == kind:
					kindListIndex.append(entry.index)
		if len(kindListIndex) == 0:
			return None
		return max(kindListIndex)

	def kindOf(self, name):
		#returns STATIC, FIELD, ARG, VAR, or NONE
		for entry in self.subroutineScope:
			if entry.name == name:
				return entry.kind
		for entry in self.classScope:
			if entry.name == name:
				return entry.kind
		return None

	def typeOf(self, name):
		#returns string
		for entry in self.subroutineScope:
			if entry.name == name:
				return entry.jackType
		for entry in self.classScope:
			if entry.name == name:
				return entry.jackType
			

	def indexOf(self, name):
		#returns int
		for entry in self.subroutineScope:
			if entry.name == name:
				return entry.index
		for entry in self.classScope:  
			if entry.name == name: 
				return entry.index			

class CompilationEngine:
	def __init__(self,tokenizer,outfile):
		self.space = 0
		self.outfile = open("{}-comp.xml".format(outfile.split('.')[0]), 'w') 
		self.t = tokenizer
		self.lastToken = None
		self.st = SymbolTable()
		self.currentClass = None
		self.currentSubroutine = None
		self.nLocals = 0
		self.nArgs = 0
		self.vmw = VMWriter("{}.vm".format(outfile.split('.')[0]))
		self.labelCount = 0
		self.firstSubroutineStatements = False

	def writeMarkupToken(self):
		self.lastToken = self.t.currentToken
		self.outfile.write(self.t.createMarkupToken())
		self.outfile.write('\n')

	def decide(self):
		if self.t.currentToken == 'class':
			self.compileClass()
		elif self.t.currentToken == 'static' or self.t.currentToken == 'field':
			self.compileClassVarDec()
		#handle function, method, and constructor here
		elif self.t.currentToken == 'function' or self.t.currentToken == 'method' or self.t.currentToken == 'constructor':
			self.compileSubroutine()
		elif self.t.currentToken == 'var':
			self.compileVarDec()
		elif self.t.currentToken == 'let' or self.t.currentToken == 'do' or self.t.currentToken == 'while' or self.t.currentToken == 'if' or self.t.currentToken == 'return':
			self.compileStatements()
		else:
			self.writeMarkupBeg('DONE!!!!!!')

	def compileClass(self):
	# format ('class', name, '{', (recurse statics, functions), '}')
		self.writeMarkupBeg('class')
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileClass IDENTIFIER: {}'.format(self.t.currentToken))
		self.currentClass = self.t.currentToken
		self.writeNadv()
		self.writeST('class', 'defined')
		if self.t.currentToken != '{':
			print('error -compileClass leftcurly : {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '}':
			self.decide()
		if self.t.currentToken != '}':
			print('error -compileClass rightcurly : {}'.format(self.t.currentToken))
		self.writeMarkupToken()
		self.writeMarkupEnd('class')
		if self.t.hasMoreTokens():
			self.t.advance()
			self.decide()

	def compileClassVarDec(self):
		self.writeMarkupBeg('classVarDec')
		if self.t.currentToken != 'static' and self.t.currentToken != 'field':
			print('error -compileClassVarDec static OR field: {}'.format(self.t.currentToken))
		kind = self.t.currentToken
		self.writeNadv()
		if self.t.tokenType() != KEYWORD:
			print('error -compileClassVarDec KEYWORD: {}'.format(self.t.currentToken))
		jackType = self.t.currentToken
		self.writeNadv()
		self.handleJackType(jackType)
		if self.t.tokenType() != IDENTIFIER:
                	print('error -compileClassVarDec IDENTIFIER: {}'.format(self.t.currentToken))
		name = self.t.currentToken
		self.st.define(name, jackType, kind)
		self.writeNadv()
		self.writeST(kind, 'defined', name)
		while self.t.currentToken != ';':
			if self.t.currentToken != ',':
				print('error -compileVarDec , : {}'.format(self.t.currentToken))
			self.writeNadv()
			if self.t.tokenType() != IDENTIFIER:
				print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
			name = self.t.currentToken
			self.st.define(name, jackType, kind)
			self.writeNadv()
			self.writeST(kind, 'defined', name)
		if self.t.currentToken != ';':
			print('error -compileClassVarDec ; : {}'.format(self.t.currentToken))
		self.writeNadv()
		#if self.t.currentToken == 'static' or self.t.currentToken == 'field':
		#	self.decide()
		#else:
		self.writeMarkupEnd('classVarDec')
		self.decide()


	def compileSubroutine(self):
		isMethod = False
		self.firstSubroutineStatements = True
		self.st.startSubroutine()
		self.writeMarkupBeg('subroutineDec')
		if self.t.currentToken != 'function' and self.t.currentToken != 'method' and self.t.currentToken != 'constructor':
			print('error -compileSubroutineDec function: {}'.format(self.t.currentToken))
		if self.t.currentToken == 'method':
			isMethod = True
		self.writeNadv()
		if self.t.tokenType() != KEYWORD:
			print('error -compileSubroutineDec KEYWORD: {}'.format(self.t.currentToken))
		jackType = self.t.currentToken
		self.writeNadv()
		self.handleJackType(jackType)
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileSubroutineDec IDENTIFIER: {}'.format(self.t.currentToken))
		self.currentSubroutine = self.t.currentToken
		self.writeNadv()
		self.writeST('subroutine', 'defined')
		if self.t.currentToken != '(':
			print('error -compileSubroutineDec leftparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		#vmw (if method push 'this'? as first arg)
		if isMethod:
			self.vmw.writePush('this', 0)
		self.compileParameterList()
		if self.t.currentToken != ')':
			print('error -compileSubroutineDec rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileSubroutineBody()
		#vmw (not sure if I want this here, but pretty sure I do)(doesn't match jack return location, but it's handled in if/else and while vm handling I think)
		self.vmw.writeReturn()
		self.writeMarkupEnd('subroutineDec')
	# possible problem here (not sure when to advance)
	#	if self.t.hasMoreTokens():
	#		self.t.advance()
		# not sure if I should be dealing with } here or in class or something else
		if self.t.currentToken != '}':
			self.decide()

	def compileSubroutineBody(self):
		self.writeMarkupBeg('subroutineBody')
		if self.t.currentToken != '{':
			print('error -compileSubroutineBody leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		# while not right curly, decide (include in decide var decs)
		while self.t.currentToken != '}':
			self.decide()
		if self.t.currentToken != '}':
			print('error -compileSubroutineBody rightcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.writeMarkupEnd('subroutineBody')
		self.labelCount = 0

	def compileParameterList(self):
		self.writeMarkupBeg('parameterList')
		while self.t.currentToken != ')':
			#check parameters
			#need to do symbol table possibly, is ARG?
			if self.t.currentToken != ',':
				self.handleParameter(True)
			else:
				self.writeNadv()
		self.writeMarkupEnd('parameterList')

	def handleParameter(self, isType, jackType = None):
		if isType:
			jackType = self.t.currentToken
			if self.t.currentToken not in KEYWORDS:
				self.writeNadv()
				self.writeST('class','used')
			else:
				self.writeNadv()
			self.handleParameter(False, jackType)
		else:
			name = self.t.currentToken
			self.st.define(name, jackType, ARG)
			self.writeNadv()
			self.writeST('lookup', 'defined', name)

	def compileVarDec(self):
		#vmw
		self.nLocals += 1
		self.writeMarkupBeg('varDec')
		if self.t.currentToken != 'var':
			print('error -compileVarDec var: {}'.format(self.t.currentToken))
		kind = self.t.currentToken
		self.writeNadv()
		# possible problem with identifier / keyword
		if self.t.tokenType() != KEYWORD and self.t.tokenType() != IDENTIFIER:
			print('error -compileVarDec IDENTIFIER or KEYWORD: {}'.format(self.t.tokenType()))
		jackType = self.t.currentToken
		self.writeNadv()
		self.handleJackType(jackType)
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
		name = self.t.currentToken
		self.st.define(name, jackType, kind)
		self.writeNadv()
		self.writeST(kind, 'defined', name)
		while self.t.currentToken != ';':
			if self.t.currentToken != ',':
				print('error -compileVarDec , : {}'.format(self.t.currentToken))
			self.writeNadv()
			self.nLocals += 1
			if self.t.tokenType() != IDENTIFIER:
				print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
			name = self.t.currentToken
			self.st.define(name, jackType, kind)
			self.writeNadv()
			self.writeST(kind, 'defined', name)
		self.writeNadv()
		self.writeMarkupEnd('varDec')
		if self.t.currentToken != '}':
			self.decide()

	def compileStatements(self):
		#vmw
		if self.firstSubroutineStatements == True:
			self.vmw.writeFunction('{}.{}'.format(self.currentClass, self.currentSubroutine), self.nLocals)
			self.firstSubroutineStatements = False
		self.writeMarkupBeg('statements')
		while self.t.currentToken != '}':
			if self.t.currentToken == 'let':
				self.compileLet()
			elif self.t.currentToken == 'do': 
				self.compileDo()
			elif self.t.currentToken == 'while':
				self.compileWhile()
			elif self.t.currentToken == 'if':
				self.compileIf()
			elif self.t.currentToken == 'return':
				self.compileReturn()
		self.writeMarkupEnd('statements')

	def compileDo(self):
		#vmr
		subroutineFullName = ''
		self.writeMarkupBeg('doStatement')
		if self.t.currentToken != 'do':
			print('error -compileDo do: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken[0].isupper():
			#function call
			#vmr
			subroutineFullName += self.t.currentToken
			self.writeNadv()
			self.writeST('class','used')
			if self.t.currentToken != '.':
				print('error -compileDo . : {}'.format(self.t.currentToken))
			subroutineFullName += self.t.currentToken
			self.writeNadv()
			#function of other class or same class
			#vmr
			subroutineFullName += self.t.currentToken
			self.writeNadv()
			self.writeST('subroutine','used')
			if self.t.currentToken != '(':
				print('error -compileDo leftparen : {}'.format(self.t.currentToken))
			self.writeNadv()
			self.compileExpressionList()
			if self.t.currentToken != ')':
				print('error -compileDo rightparen : {}'.format(self.t.currentToken))
			self.writeNadv()
		elif self.t.currentToken[0].islower():
			#method call
			name = self.t.currentToken
			#vmw
			subroutineFullName += self.t.currentToken
			self.writeNadv()
			if self.t.currentToken == '(':
				self.writeST('subroutine','used')
				#method call of current class	
				self.writeNadv()
				self.compileExpressionList()
				if self.t.currentToken != ')':
					print('error -compileDo rightparen : {}'.format(self.t.currentToken))
				self.writeNadv()
			elif self.t.currentToken == '.':
				#writing here so 'lookup' isn't used when calling method on current class
				self.writeST('lookup','used',name)
				#method call of different object
				#vmw
				subroutineFullName += self.t.currentToken
				self.writeNadv()
				#method of different class on lower case object
				#vmw
				subroutineFullName += self.t.currentToken
				self.writeNadv()
				self.writeST('subroutine','used')
				if self.t.currentToken != '(':
					print('error -compileDo leftparen : {}'.format(self.t.currentToken))
				self.writeNadv()
				self.compileExpressionList()
				if self.t.currentToken != ')':
					print('error -compileDo rightparen : {}'.format(self.t.currentToken))
				self.writeNadv()
			else:
				print('error -compileDo leftparen or . : {}'.format(self.t.currentToken))
		else:
			print('error -compileDo not function or method: {}'.format(self.t.currentToken))
		if self.t.currentToken != ';':
			print('error -compileDo ; : {}'.format(self.t.currentToken))
		self.writeNadv()
		self.writeMarkupEnd('doStatement')
		#self.decide()
		#vmw
		self.vmw.writeCall(subroutineFullName, self.nArgs)
		self.nArgs = 0
		self.vmw.writePop('temp', 0)

	def compileLet(self):
		self.writeMarkupBeg('letStatement')
		if self.t.currentToken != 'let':
			print('error -compileLet let: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileLet IDENTIFIER: {}'.format(self.t.currentToken))
		# vmw and ST, and compilationEngine
		kind, index = self.compileIdentifier()
		if self.t.currentToken != '=':
			print('error -compileLet = : {}'.format(self.t.currentToken))
		self.writeNadv()
		#maybe compileExpressionList() if I find out there can be 'let a,b = (2+1),(4+2)'
		self.compileExpression(';')
		if self.t.currentToken != ';':
			print('error -compileLet ; : {}'.format(self.t.currentToken))
		self.writeNadv()
		self.writeMarkupEnd('letStatement')
		#self.decide()
		#vmw
		self.vmw.writePop(kind, index)
		

	def compileWhile(self):
		#include brackets, and either decide() or compileStatements()
		self.writeMarkupBeg('whileStatement')
		if self.t.currentToken != 'while':
			print('error -compileWhile while: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '(':
			print('error -compileWhile leftparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		#vmw
		firstLocalLabel = self.getLabel()
		self.vmw.writeLabel(firstLocalLabel)
		self.compileExpression(')')
		#vmw
		self.vmw.writeArithmetic('~', 'unary')
		secondLocalLabel = self.getLabel()
		self.vmw.writeIf(secondLocalLabel)
		if self.t.currentToken != ')':
			print('error -compileWhile rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '{':
			print('error -compileWhile leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		# decide or comp statements
		self.compileStatements()
		#vmw
		self.vmw.writeGoto(firstLocalLabel)
		if self.t.currentToken != '}':
			print('error -compileWhile rightcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.writeMarkupEnd('whileStatement')
		#self.decide()
		#vmw
		self.vmw.writeLabel(secondLocalLabel)

	def compileReturn(self):
		self.writeMarkupBeg('returnStatement')
		# probably will need to handle expressions
		if self.t.currentToken != 'return':
			print('error -compileReturn return: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken == ';':
			self.writeNadv()
			#vmw (not sure if this is correct)
			self.vmw.writePush('constant', 0)
		else:
			self.compileExpression(';')
			if self.t.currentToken != ';':
				print('error -compileReturn ; : {}'.format(self.t.currentToken))
			self.writeNadv()
		self.writeMarkupEnd('returnStatement')
		#vmw
		self.nLocals = 0

	def compileIf(self):
		# include else and brackets, and either decide() or compileStatements()
		self.writeMarkupBeg('ifStatement')		
		if self.t.currentToken != 'if':
			print('error -compileIf if : {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '(':
			print('error -compileIf leftparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileExpression(')')
		#vmw
		self.vmw.writeArithmetic('~', 'unary')
		firstLocalLabel = self.getLabel()
		self.vmw.writeIf(firstLocalLabel)
		if self.t.currentToken != ')':
			print('error -compileIf rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '{':   
			print('error -compileIf leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
                # decide or comp statements
		self.compileStatements()
		#vmw
		secondLocalLabel = self.getLabel()
		self.vmw.writeGoto(secondLocalLabel)
		if self.t.currentToken != '}':							
			print('error -compileIf rightcurly: {}'.format(self.t.currentToken))	
		self.writeNadv()
		if self.t.currentToken == 'else':
			#vmw
			self.vmw.writeLabel(firstLocalLabel)
			self.compileElse()
			#vmw
			self.vmw.writeLabel(secondLocalLabel)
		else:
			self.vmw.writeLabel(firstLocalLabel)
			self.vmw.writeLabel(secondLocalLabel)
		self.writeMarkupEnd('ifStatement')   
		#self.decide()

	def compileElse(self):
		self.writeNadv()
		if self.t.currentToken != '{':
			print('error -compileElse leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileStatements()
		if self.t.currentToken != '}':
			print('error -compileElse rightcurly: {}'.format(self.t.currentToken))
		self.writeNadv()

	def compileExpression(self, ender):
		self.writeMarkupBeg('expression')
		# all of expression is gonna need some work
		while self.t.currentToken != ender and self.t.currentToken != ',':
			if self.lastToken != ',' and self.lastToken != '(' and self.isBooleanOperator():
				#vmw
				binaryOperator = self.t.currentToken
				self.writeNadv()
				#vmw (added compileTerm here too, to achieve post-fix for VM)(or compileExpression?)
				self.compileTerm()
				self.vmw.writeArithmetic(binaryOperator, 'binary')
			else:
				self.compileTerm()
		self.writeMarkupEnd('expression')

	def compileTerm(self):
		self.writeMarkupBeg('term')
		if self.t.currentToken == '-' or self.t.currentToken == '~':
			#vmw
			unaryOperator = self.t.currentToken
			self.writeNadv()
			self.compileTerm()
			#vmw
			self.vmw.writeArithmetic(unaryOperator, 'unary')
		elif self.t.currentToken == '(':
			self.writeNadv()
			self.compileExpression(')')
			# ')'
			self.writeNadv()
		else:
			name = self.t.currentToken
			#vmw (might need to add more here)
			kind, index = self.getKindIndex()
			if self.t.currentToken.isnumeric():
				self.vmw.writePush('constant', int(self.t.currentToken))
			elif self.t.currentToken == 'null' or self.t.currentToken == 'false':
				self.vmw.writePush('constant', 0)
			elif self.t.currentToken == 'true':
				self.vmw.writePush('constant', 1)
				self.vmw.writeArithmetic('-', 'unary')
			#else:
			#	self.vmw.writePush(kind, index)
			self.writeNadv()
			if self.t.currentToken == '.' or self.t.currentToken == '(':
				self.writeST('class','used')
				#vmw and ST
				self.compileRestFunctionOrMethodCall(name)
			elif self.t.currentToken == '[':
				self.writeST('lookup','used',name)
				#vmw and ST (still need to do this for vmw)
				self.compileArrayElement()
			else:
				#write symbol table findings if in scope and not array or subroutine call
				self.writeSTifInScope(name)
				#vmw (should this always be a push?) 
				if kind != None:
					self.vmw.writePush(kind, index)
		self.writeMarkupEnd('term')

	def isBooleanOperator(self):
		operators = ['*', '+', '-', '/', '|', '&', '<','>','=']
		for operator in operators:
			if self.t.currentToken == operator:
				return True
		return False

	def compileArrayElement(self):
		# '['
		self.writeNadv()
		self.compileExpression(']')
		# ']'
		self.writeNadv()

	def compileRestFunctionOrMethodCall(self, firstPart):
		hadPeriod = False
		if self.t.currentToken == '.':
			hasPeriod = True
			# '.'
			self.writeNadv()
			# function or method name
			name = self.t.currentToken
			self.writeNadv()
			self.writeST('subroutine','used')
		# '('
		self.writeNadv()
		self.compileExpressionList()
		# ')'
		#vmr
		if hasPeriod:
			#need to finish this
			
			subroutineName = '{}.{}'.format(firstPart, name)
		else:
			subroutineName = '{}.{}'.format(self.currentClass, firstPart)
		self.vmw.writeCall(subroutineName, self.nArgs)
		self.nArgs = 0
		self.writeNadv()

	def compileExpressionList(self):
		self.writeMarkupBeg('expressionList')
		while self.t.currentToken != ')':
			if self.t.currentToken == ',':
				self.writeNadv()
			self.compileExpression(')')
			self.nArgs += 1
		self.writeMarkupEnd('expressionList')

	def compileIdentifier(self):
		name = self.t.currentToken
		kind = self.st.kindOf(name)
		if kind == None:
			print('var {} not found'.format(name))
		else:
			index = self.st.indexOf(name)
		self.writeNadv()
		self.writeST('lookup','used',name)
		if self.t.currentToken == '[':
			self.writeNadv()
			self.compileExpression(']')
			if self.t.currentToken != ']':
				print('error -compileIdentifier rightbracket: {}'.format(self.t.currentToken))
			self.writeNadv()
		#vmw (this might get hairy because I call self.writeNadv() here, too)
		return kind, index

	def handleJackType(self, keywordOrId):
		if keywordOrId not in KEYWORDS:
			self.writeST('class', 'used')

	def getLabel(self):
		print(self.labelCount)
		label = '{}-{}-{}'.format(self.currentClass,self.currentSubroutine,self.labelCount)
		self.labelCount += 1
		return label

	def writeMarkupBeg(self, text):
		self.outfile.write('<{}>'.format(text))
		self.outfile.write('\n')

	def writeMarkupEnd(self, text):
		self.outfile.write('</{}>'.format(text))
		self.outfile.write('\n')
	
	def writeNadv(self):
		self.writeMarkupToken()
		self.t.advance()

	def writeSTifInScope(self, name):
		if self.st.kindOf(name) != None:
			self.writeST('lookup','used',name)

	def getKindIndex(self):
		kind = self.st.kindOf(self.t.currentToken)
		index = self.st.indexOf(self.t.currentToken)
		return kind, index

	def writeST(self, category, definedOrUsed, name=None):
		if category == 'lookup':
			category = self.st.kindOf(name)
		self.outfile.write('category: {}'.format(category))
		self.outfile.write('\n')
		self.outfile.write('defined or used: {}'.format(definedOrUsed))
		self.outfile.write('\n')
		if category != 'class' and category != 'subroutine':
			self.outfile.write('its a variable \n')
			self.outfile.write('index: {}'.format(self.st.indexOf(name)))
			self.outfile.write('\n')

#the compilation engine should create, write to, and close a new VMWriter for each .jack file(or each class?) it recieves
class VMWriter:
	def __init__(self, outfile):
		#create .vm file
		self.outfile = open(outfile, 'w')

	def writePush(self, segment, index):
		if segment == VAR:
			segment = LOCAL
		if segment == FIELD:
			segment = THIS
		#segment is constant, argument, local, static, this, that, pointer, temp, index is integer
		self.outfile.write('push {} {}'.format(segment, index))
		self.outfile.write('\n')

	def writePop(self, segment, index):
		if segment == VAR:
			segment = LOCAL
		if segment == FIELD:
			segment = THIS
		self.outfile.write('pop {} {}'.format(segment, index))
		self.outfile.write('\n')

	def writeArithmetic(self, command, opType):
		#command is add, sub, neg, eq, gt, lt, and, or, not
		if command not in ['+', '-', '=', '>', '<', '&', '|', '~']:
			self.writeCall(command, 2)
		else:
			if command == '+':
				self.outfile.write('add')
			elif command == '-' and opType == 'binary':
				self.outfile.write('sub')
			elif command == '-' and opType == 'unary':
				self.outfile.write('neg')
			elif command == '=':
				self.outfile.write('eq')
			elif command == '>':
				self.outfile.write('gt')
			elif command == '<':
				self.outfile.write('lt')
			elif command == '&':
                        	self.outfile.write('and')
			elif command == '|':
                        	self.outfile.write('or')
			elif command == '~':
				self.outfile.write('not')
			self.outfile.write('\n')
	
	def writeLabel(self, label):
		self.outfile.write('label {}'.format(label))
		self.outfile.write('\n')

	def writeGoto(self, label):
		self.outfile.write('goto {}'.format(label))
		self.outfile.write('\n')

	def writeIf(self, label):
		#write if-goto
		self.outfile.write('if-goto {}'.format(label))
		self.outfile.write('\n')

	def writeCall(self, name, nArgs):
		#VM call command
		if name == '*':
			self.writeCall('Math.multiply', nArgs)
		elif name == '/':
			self.writeCall('Math.divide', nArgs)
		else:
			self.outfile.write('call {} {}'.format(name, nArgs))
		self.outfile.write('\n')

	def writeFunction(self, name, nLocals):
		#VM function command
		self.outfile.write('function {} {}'.format(name, nLocals))
		self.outfile.write('\n')


	def writeReturn(self):
		#VM return command
		self.outfile.write('return')
		self.outfile.write('\n')

	def close(self):
		self.outfile.close()



if __name__ == '__main__':
	path = sys.argv[-1].split('/')[0]
	if os.path.isdir(path):
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		onlyJackfiles = list(filter(lambda x: x[-5:] == '.jack', onlyfiles))
		onlyJackfilesPath = list(map(lambda x : '{}/{}'.format(path,x), onlyJackfiles))
		for filepath in onlyJackfilesPath:
			print(filepath)
			mainProcess(filepath)
			
	elif os.path.isfile(path):
		mainProcess(path)

