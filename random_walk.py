from markov import Markov
from cleaner import *
from random import *

class RandomWalk(Markov):
	def __init__(self, corpus, order):
		Markov.__init__(self, corpus, order)
		self.nextDict = {}
		self.stoppers = getStop(self)
		self.starters = getStart(self)

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

	def randomWord(self):
		counter = 0
		random = randrange(0, nextDict)
		for key in self.nextDict:
			if counter > random:
				return key
			else:
				counter += self.nextDict[key]
		if counter > random:
			return key
		else:
			raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def randomWalk(model):
		self.nextDict
		sentance = []
		starters = filter_dict(model.dict, starter(model.dict))
		stoppers = filter_dict(model.dict, stopper(model.dict))
		first = randomWord(starters)
		sentance.append(first)
		sentance.append(randomWord(model.dict))
		print(sentance)

		orderMod = model.order
		while orderMod > 1:


if __name__ == '__main__':
	fishy = "One fish two fish, red fish. Blue fish."
	model = Markov(fishy, 3)
	randomWalk(model)