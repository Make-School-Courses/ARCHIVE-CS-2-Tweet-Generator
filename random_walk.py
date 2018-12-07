from markov import Markov
from random import *

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

if __name__ == '__main__':
	fishy = "one fish two fish red fish blue fish"
	model = Markov(fishy, 1)
	print(random_walk(model))
