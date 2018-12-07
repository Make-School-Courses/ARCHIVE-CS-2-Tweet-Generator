from markov import Markov
from random import *

class RandomWalk(object):
	def __init__(order):
		self.sentance = ''

	def random_walk(model):
		counter = 0
		random = randrange(0, model.tokens)
		for key in model.dict:
			if counter > random:
				return key
			else:
				counter += model.dict[key]
		else:
			raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def parser(word):
		if word[0] == "<":
			pass
		elif word[len(word)] == ">":
			pass
		else:
			pass



if __name__ == '__main__':
	fishy = "one fish two fish red fish blue fish"
	model = Markov(fishy, 2)
	print(random_walk(model))