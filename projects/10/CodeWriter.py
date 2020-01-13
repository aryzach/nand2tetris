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

STATIC = 'static'
FIELD = 'field'
VAR = 'local'
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
	ce = CompilationEngine(ct,"{}-comp.xml".format(filepath.split('.')[0]))
	print(ct.allTokens)
#	while ct.hasMoreTokens():
#		ct.advance()
#		ct.writeMarkupToken()
#	ct.writeExplicit('</tokens>')
	if ct.hasMoreTokens():
		ct.advance()
		ce.decide()
	ct.close()

class STentry:
	def __init__(self, name, jackType, kind):
		self.name = name
		self.jackType = jackType
		self.kind = kind
		self.index = None

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
				if entry.kind = kind:
					kindListIndex.append(entry.index)
		elif kind == VAR or kind == ARG:
			for entry in self.subroutineScope:
				if entry.kind = kind:
					kindListIndex.append(entry.index)
		if len(kindListIndex) == 0:
			return None
		return max(kindListIndex)

	def kindOf(self, name):
		#returns STATIC, FIELD, ARG, VAR, or NONE
		for entry in self.subroutineScope:
			if entry.name = name:
				return entry.kind
		for entry in self.classScope:
			if entry.name = name:
				return entry.kind
		return None

	def typeOf(self, name):
		#returns string
		for entry in self.subroutineScope:
			if entry.name = name:
				return entry.jackType
		for entry in self.classScope:
			if entry.name = name:
				return entry.jackType
			

	def indexOf(self, name):
		#returns int
		for entry in self.subroutineScope:
			if entry.name = name:
				return entry.index
                for entry in self.classScope:  
			if entry.name = name: 
				return entry.index			

class CompilationEngine:
	def __init__(self,tokenizer,outfile):
		self.space = 0
		self.outfile = open(outfile, 'w') 
		self.t = tokenizer
		self.lastToken = None

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
		self.writeNadv()
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
		self.writeNadv()
		if self.t.tokenType() != KEYWORD:
			print('error -compileClassVarDec KEYWORD: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
                	print('error -compileClassVarDec IDENTIFIER: {}'.format(self.t.currentToken))
		self.writeNadv()
		while self.t.currentToken != ';':
			if self.t.currentToken != ',':
				print('error -compileVarDec , : {}'.format(self.t.currentToken))
			self.writeNadv()
			if self.t.tokenType() != IDENTIFIER:
				print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
			self.writeNadv()
		if self.t.currentToken != ';':
			print('error -compileClassVarDec ; : {}'.format(self.t.currentToken))
		self.writeNadv()
		#if self.t.currentToken == 'static' or self.t.currentToken == 'field':
		#	self.decide()
		#else:
		self.writeMarkupEnd('classVarDec')
		self.decide()


	def compileSubroutine(self):
		self.writeMarkupBeg('subroutineDec')
		if self.t.currentToken != 'function' and self.t.currentToken != 'method' and self.t.currentToken != 'constructor':
			print('error -compileSubroutineDec function: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.tokenType() != KEYWORD:
			print('error -compileSubroutineDec KEYWORD: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileSubroutineDec IDENTIFIER: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '(':
			print('error -compileSubroutineDec leftparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileParameterList()
		if self.t.currentToken != ')':
			print('error -compileSubroutineDec rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileSubroutineBody()
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

	def compileParameterList(self):
		self.writeMarkupBeg('parameterList')
		while self.t.currentToken != ')':
			#check parameters
			self.writeNadv()
		self.writeMarkupEnd('parameterList')

	def compileVarDec(self):
		self.writeMarkupBeg('varDec')
		if self.t.currentToken != 'var':
			print('error -compileVarDec var: {}'.format(self.t.currentToken))
		self.writeNadv()
		# possible problem with identifier / keyword
		if self.t.tokenType() != KEYWORD and self.t.tokenType() != IDENTIFIER:
			print('error -compileVarDec IDENTIFIER or KEYWORD: {}'.format(self.t.tokenType()))
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
		self.writeNadv()
		while self.t.currentToken != ';':
			if self.t.currentToken != ',':
				print('error -compileVarDec , : {}'.format(self.t.currentToken))
			self.writeNadv()
			if self.t.tokenType() != IDENTIFIER:
				print('error -compileVarDec IDENTIFIER: {}'.format(self.t.currentToken))
			self.writeNadv()
		self.writeNadv()
		self.writeMarkupEnd('varDec')
		if self.t.currentToken != '}':
			self.decide()

	def compileStatements(self):
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
		self.writeMarkupBeg('doStatement')
		if self.t.currentToken != 'do':
			print('error -compileDo do: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken[0].isupper():
			#function call
			self.writeNadv()
			if self.t.currentToken != '.':
				print('error -compileDo . : {}'.format(self.t.currentToken))
			self.writeNadv()
			#function of other class or same class
			self.writeNadv()
			if self.t.currentToken != '(':
				print('error -compileDo leftparen : {}'.format(self.t.currentToken))
			self.writeNadv()
			self.compileExpressionList()
			if self.t.currentToken != ')':
				print('error -compileDo rightparen : {}'.format(self.t.currentToken))
			self.writeNadv()
		elif self.t.currentToken[0].islower():
			#method call
			self.writeNadv()
			if self.t.currentToken == '(':
				#method call of current class
				self.writeNadv()
				self.compileExpressionList()
				if self.t.currentToken != ')':
					print('error -compileDo rightparen : {}'.format(self.t.currentToken))
				self.writeNadv()
			elif self.t.currentToken == '.':
				#method call of different object
				self.writeNadv()
				#method of different class on lower case object
				self.writeNadv()
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

	def compileLet(self):
		self.writeMarkupBeg('letStatement')
		if self.t.currentToken != 'let':
			print('error -compileLet let: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.tokenType() != IDENTIFIER:
			print('error -compileLet IDENTIFIER: {}'.format(self.t.currentToken))
		self.compileIdentifier()
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

	def compileWhile(self):
		#include brackets, and either decide() or compileStatements()
		self.writeMarkupBeg('whileStatement')
		if self.t.currentToken != 'while':
			print('error -compileWhile while: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '(':
			print('error -compileWhile leftparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.compileExpression(')')
		if self.t.currentToken != ')':
			print('error -compileWhile rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '{':
			print('error -compileWhile leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		# decide or comp statements
		self.compileStatements()
		if self.t.currentToken != '}':
			print('error -compileWhile rightcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
		self.writeMarkupEnd('whileStatement')
		#self.decide()

	def compileReturn(self):
		self.writeMarkupBeg('returnStatement')
		# probably will need to handle expressions
		if self.t.currentToken != 'return':
			print('error -compileReturn return: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken == ';':
			self.writeNadv()
		else:
			self.compileExpression(';')
			if self.t.currentToken != ';':
				print('error -compileReturn ; : {}'.format(self.t.currentToken))
			self.writeNadv()
		self.writeMarkupEnd('returnStatement')

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
		if self.t.currentToken != ')':
			print('error -compileIf rightparen: {}'.format(self.t.currentToken))
		self.writeNadv()
		if self.t.currentToken != '{':   
			print('error -compileIf leftcurly: {}'.format(self.t.currentToken))
		self.writeNadv()
                # decide or comp statements
		self.compileStatements()
		if self.t.currentToken != '}':							
			print('error -compileIf rightcurly: {}'.format(self.t.currentToken))	
		self.writeNadv()
		if self.t.currentToken == 'else':
			self.compileElse()
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
			if self.lastToken != '(' and self.isBooleanOperator():
				self.writeNadv()
			else:
				self.compileTerm()
		self.writeMarkupEnd('expression')

	def compileTerm(self):
		self.writeMarkupBeg('term')
		if self.t.currentToken == '-' or self.t.currentToken == '~':
			self.writeNadv()
			self.compileTerm()
		elif self.t.currentToken == '(':
			self.writeNadv()
			self.compileExpression(')')
			# ')'
			self.writeNadv()
		else:
			self.writeNadv()
			if self.t.currentToken == '.' or self.t.currentToken == '(':
				self.compileRestFunctionOrMethodCall()
			elif self.t.currentToken == '[':
				self.compileArrayElement()
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

	def compileRestFunctionOrMethodCall(self):
		if self.t.currentToken == '.':
			# '.'
			self.writeNadv()
			# function or method name
			self.writeNadv()
		# '('
		self.writeNadv()
		self.compileExpressionList()
		# ')'
		self.writeNadv()

	def compileExpressionList(self):
		self.writeMarkupBeg('expressionList')
		while self.t.currentToken != ')':
			if self.t.currentToken == ',':
				self.writeNadv()
			self.compileExpression(')')
		self.writeMarkupEnd('expressionList')

	def compileIdentifier(self):
		self.writeNadv()
		if self.t.currentToken == '[':
			self.writeNadv()
			self.compileExpression(']')
			if self.t.currentToken != ']':
				print('error -compileIdentifier rightbracket: {}'.format(self.t.currentToken))
			self.writeNadv()

	def writeMarkupBeg(self, text):
		self.outfile.write('<{}>'.format(text))
		self.outfile.write('\n')

	def writeMarkupEnd(self, text):
		self.outfile.write('</{}>'.format(text))
		self.outfile.write('\n')
	
	def writeNadv(self):
		self.writeMarkupToken()
		self.t.advance()

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

