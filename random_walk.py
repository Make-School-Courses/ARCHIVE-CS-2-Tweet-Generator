from markov import Markov
from cleaner import *
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

def stoppers(dict):
	tokens = []
	print(dict)
	for key in dict:
		val = dict[key]
		if key[len(key)-1].endswith('.'):
			print("word with . ", key)
			tokens.append(key)
	return tokens

def starters(dict):
	tokens = []
	for key in dict:
		val = dict[key]
		if key[0][0].isupper():
			print("capitalized Word ", key)
			tokens.append(key)
	return tokens

if __name__ == '__main__':
	fishy = "One fish two fish, red fish blue fish."
	model = Markov(fishy, 3)
	print(stoppers(model.dict))
	print(starters(model.dict))