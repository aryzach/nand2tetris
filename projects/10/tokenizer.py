import sys
import os
from os import listdir
from os.path import isfile, join
import glob
import re

SYMBOLS = ';{}&]-/=~'
REST_SYMBOLS = '|().[<>+*'

class Tokenizer:
	def __init__(self, infile):
		self.currentToken = None
		self.origTokens = None
		self.separate(infile)
		self.allTokens = None

	def separate(self,infile):
		withInlineComments = list(filter(lambda x : (x[0] != '/'),open(infile, 'r').readlines()))
		woInlineComments = []
		for line in withInlineComments:
			for part in list(filter(lambda x : (len(x) > 0),line.split('/', 1))):
				if part[0] != '/':
					woInlineComments.append(part.strip())			
		noComments = list(filter(lambda x : (len(x) > 0), woInlineComments))
		tokensDraft = []
		for line in noComments:
			for word in line.split():
				tokensDraft.append(word)
		self.allTokens = tokensDraft
		for symbol in SYMBOLS:
			print("THIS IS SYMBOL {}".format(symbol))
			self.seperateTokensOnSymbol(self.allTokens, symbol)
		for symbol in REST_SYMBOLS:
			print("THIS IS SYMBOL {}".format(symbol))
			self.seperateTokensOnRestSymbol(self.allTokens, symbol)
			print(self.allTokens)
	def seperateTokensOnRestSymbol(self, allCurrentTokens, symbol):
		tempTokens = []
		for thing in allCurrentTokens:
			if symbol in thing:
				print(thing)
				numSyb = 0
				splitThing = []
				for letter in thing:
					if letter == symbol:
						splitThing.append(symbol)
						numSyb += 2
						print(splitThing)
					else:
						splitThing.append('')
						splitThing.append('')
						splitThing[numSyb] += letter
				tempTokens = tempTokens + splitThing
			else:
				tempTokens.append(thing)
		self.allTokens = list(filter(lambda x : (len(x)>0),tempTokens))

	def seperateTokensOnSymbol(self, allCurrentTokens, symbol):
		tempTokens = []
		for thing in allCurrentTokens:
			print(thing)
			for item in list(filter(lambda x : (len(x)>0),re.split('({})'.format(symbol), thing))):
				tempTokens.append(item)
		self.allTokens = tempTokens


	def hasMoreTokens(self):
		return True

	def advance(self):
		#get next token and make it the current token
		return None

	def tokenType(self):
		return ''
	"""	KEYWORD 
		SYMBOL
		IDENTIFIER
		INT_CONST
		STRING_CONST
		return tokenType
	"""	

	def keyWord(self):
		return None
	"""	CLASS
		METHOD
		CONSTRUCTOR
		FUNCTION
		INT
		BOOL
		CHAR
		VOID
		NULL
		VAR
		STATIC
		FIELD
		LET
		DO
		IF
		ELSE
		WHILE
		RETURN
		TRUE
		FALSE
		THIS
	"""	

	def symbol(self):
		return Char

	def identifier(self):
		return String

	def intVal(self):
		return 1

	def stringVal(self):
		return ''

	def close(self):
		return None
		#close file

def mainProcess(filepath):
	ct = Tokenizer(filepath)
	while ct.hasMoreTokens():
		ct.advance()
		ct.createMarkupToken()
		ct.writeMarkupToken()
	ct.close()

if __name__ == '__main__':
	path = sys.argv[-1].split('/')[0]
	if os.path.isdir(path):
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		onlyJackfiles = list(filter(lambda x: x[-5:] == '.jack', onlyfiles))
		onlyJackfilesPath = list(map(lambda x : '{}/{}'.format(path,x), onlyJackfiles))
		for filepath in onlyJackfilesPath:
			mainProcess(filepath)
	elif os.path.isfile(path):
		mainProcess(path)

