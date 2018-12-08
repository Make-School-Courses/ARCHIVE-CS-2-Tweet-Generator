from random import *
from cleaner import *
from markov import *

class RandomWalk(MarkovChain):
	def __init__(self, corpus, order):
		# import Markov Chain ⛓
		MarkovChain.__init__(self, corpus, order)
		# initialize 'empty' variables
		self.sentance = []
		self.vocab = {}
		self.subTypes = 0
		self.subTokens = 0
		self.subPhrase = ()
		# call stoppers and starters
		self.stoppers = self.getStop()
		self.starters = self.getStart()
		# finally call randomWalk()
		self.randomWalk()

	# # # # # #

	def getStart(self):
		types = []
		for key in self.dict:
			if key[0][0].isupper():
				types.append(key)
		return types

	def getStop(self):
		types = []
		for key in self.dict:
			if key[len(key)-1].endswith('.'):
				types.append(key)
		return types

	# # # # # #

	def filterDict(self, sample, intersect = True):
		self.vocab = self.dict.copy()
		self.subTokens = self.tokens
		self.subTypes = self.types
		if intersect:
			for key in self.dict:
				if key not in sample: # not in sample
					self.subTokens -= self.vocab[key]
					self.subTypes -= 1
					del self.vocab[key]
		else:
			for key in self.dict:
				if key in sample: # must be in sample
					self.subTokens -= self.vocab[key]
					self.subTypes -= 1
					del self.vocab[key]

	def filterPhrase(self):
		self.vocab = self.dict.copy()
		self.subTokens = self.tokens
		self.subTypes = self.types
		if self.order > 0:
			index = self.order - 1
			for key in self.dict:
				while index > 0:
					if self.subPhrase[index] != key[index - 1]:
						self.subTokens -= self.vocab[key]
						self.subTypes -= 1
						del self.vocab[key]
						break
					index -= 1

	# # # # # #

	def randomWord(self):
		counter = 0
		random = randrange(self.subTokens+1)
		# print(f'\n========\ncounter {counter}')
		# print(f'random {random}')
		for key in self.vocab:
			counter += self.vocab[key]
			# print(f'\n--------\ncounter {counter}')
			# print(f'key: {key}')
			if counter >= random:
				return key
		else:
			raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def randomWalk(self):
		self.filterDict(self.starters)
		# print(f'vocab: {self.vocab}')
		while self.subPhrase not in self.stoppers:
			self.subPhrase = self.randomWord()
			self.saveToSentance()
			self.filterPhrase()
			print(self.vocab)
			# print(f'phrase: {self.subPhrase}')
		self.sentance = ' '.join(self.sentance)

	# # # # # #

	def saveToSentance(self):
		for word in self.subPhrase:
			self.sentance.append(word)

if __name__ == '__main__':
	fishy = "One fish two fish red fish blue fish."
	Engine = RandomWalk(fishy, 3)
	print(Engine.sentance)