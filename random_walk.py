from markov import Markov
from cleaner import *
from random import *

class RandomWalk(Markov):
	def __init__(self, corpus, order):
		Markov.__init__(self, corpus, order)
		self.filtered = {}
		self.stoppers = self.getStop()
		self.starters = self.getStart()
		self.sentance = []
		self.old = ''

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

	def getPhrase(self):
		types = []
		for key in self.dict:
			index = len(key) - 1
			while index > 0:
				if key[index] == self.old[index - 1]:
					print(f'old: {self.old}  |  key: {key}')
				else:
					break
				index -= 1
				if index == 0:
					types.append(key)
		print(types)
		return types

	def filterDict(self, tokens):
		self.filtered = self.dict.copy()
		for key in self.dict:
			if key not in tokens:
				del self.filtered[key]

	def filterDictRm(self, tokens):
		self.filtered = self.dict.copy()
		for key in self.dict:
			if key in tokens:
				del self.filtered[key]

	def getHistLen(self):
		length = 0
		for key in self.filtered:
			length += self.filtered[key]
		return length

	def randomWord(self):
		counter = 0
		tokens = self.getHistLen()
		random = randrange(0, tokens)
		for key in self.filtered:
			if counter >= random:
				return key
			else:
				counter += self.filtered[key]
		if counter > random:
			return key
		else:
			raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def addToSentance(self, phrase):
		for word in phrase:
			self.sentance.append(word)
		self.old = phrase
		print(self.sentance)

	def randomWalk(self):
		self.filterDict(self.starters)
		firstWord = self.randomWord()
		self.addToSentance(firstWord)
		self.filterDictRm(self.starters)
		while self.old not in self.stoppers:
			nextWord = self.randomWord()
			print(nextWord)
			self.addToSentance(nextWord)

if __name__ == '__main__':
	fishy = "One fish two fish, red fish. Blue fish red green."
	Walk = RandomWalk(fishy, 2)
	Walk.randomWalk()