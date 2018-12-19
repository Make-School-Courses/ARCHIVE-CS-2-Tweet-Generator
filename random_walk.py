'''
	This file is feature complete.
	The class outputs a Random Walk using the markov chain.
	Its optimization and functionality can likely can be improved.
	Its syntatic variable names can likely be improved.
'''

from random import *
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
		self.distribution = self.getDistribution()
		# finally call randomWalk()
		self.randomWalk()

	# # # # # #

	def getStart(self):
		types = []
		for key in self.dict:
			if key[0] !='' and key[0][0].isupper():
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
		if intersect: # keep only these items in dictionary
			# clear the temporary dict
			self.subTokens = 0
			self.subTypes = 0
			self.vocab = {}
			# add matching items to dict
			for phrase in sample:
				self.subTokens += self.dict[phrase]
				self.subTypes += 1
				self.vocab[phrase] = self.dict[phrase]
		else: # remove items from dictionary
			# create a copy of the whole dict
			self.vocab = self.dict.copy()
			self.subTokens = self.tokens
			self.subTypes = self.types
			# remove items from the dict
			for phrase in sample:
				self.subTokens -= self.vocab[phrase]
				self.subTypes -= 1
				del self.vocab[phrase]

	def filterPhrase(self):
		self.vocab = self.dict.copy()
		self.subTokens = self.tokens
		self.subTypes = self.types
		if self.order > 0:
			for key in self.dict:
				index = self.order - 1
				# print('\n----------')
				# print(f'phs: {self.subPhrase}')
				# print(f'key: {key}')
				while index > 0:
					if self.subPhrase[index] != key[index - 1]:
						# print('x')
						self.subTokens -= self.vocab[key]
						self.subTypes -= 1
						del self.vocab[key]
						break
					index -= 1

	# # # # # # # # # # # # # # # #
	# def randomWordByCount(self):
	# 	counter = 0
	# 	random = randrange(self.subTokens+1)
	# 	for key in self.vocab:
	# 		counter += self.vocab[key]
	# 		if counter >= random:
	# 			return key
	# 	else:
	# 		raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def randomWordByProb(self):
		counter = 0
		random = randrange(self.subTokens+1) / self.subTokens
		# returns a range 0 < n ≤ 1
		for key in self.vocab:
			counter += self.vocab[key] / self.subTokens
			if counter >= random:
				return key
		else:
			raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def randomWalk(self):
		self.filterDict(self.starters)
		# print(f'vocab: {self.vocab}')
		self.subPhrase = self.randomWordByProb()
		for word in self.subPhrase:
			self.sentance.append(word)
		self.filterPhrase()
		while self.subPhrase not in self.stoppers:
			self.subPhrase = self.randomWordByProb()
			self.sentance.append(self.subPhrase[len(self.subPhrase) - 1])
			self.filterPhrase()
			# print(self.vocab)
		self.sentance = ' '.join(self.sentance)

	# # # # # #

	def getDistribution(self):
		# WARNING: this function is displayed in permille, not percent!!!
		# That means that 1000‰ = 1. Again, 1‰ ≠ 1%!!!
		string = ''
		for key in self.dict:
			value = self.dict[key] / self.tokens * 1000
			string += f'{key}: {value}‰\n'
		return string


if __name__ == '__main__':
	fishy = "One fish two fish red fish blue fish."
	Engine = RandomWalk(fishy, 3)
	print(Engine.distribution)
	print(Engine.sentance)