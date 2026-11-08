"""
This file is feature complete.
The class outputs a Random Walk using the markov chain.
Its optimization and functionality can likely can be improved.
Its syntatic variable names can likely be improved.
"""

from random import randrange
from typing import Dict, Iterable, List, Tuple

from .markov import MarkovChain


class RandomWalk(MarkovChain):
	def __init__(self, corpus: str, order: int) -> None:
		# import Markov Chain ⛓
		MarkovChain.__init__(self, corpus, order)
		# initialize 'empty' variables
		self.sentance: str = ""
		self.vocab: Dict[Tuple[str, ...], int] = {}
		self.subTypes: int = 0
		self.subTokens: int = 0
		self.subPhrase: Tuple[str, ...] = ()
		# call stoppers and starters
		self.stoppers: List[Tuple[str, ...]] = self.getStop()
		self.starters: List[Tuple[str, ...]] = self.getStart()
		if not self.starters:
			raise ValueError("corpus must contain at least one word")
		if not self.stoppers:
			raise ValueError("corpus must contain sentence-ending punctuation")
		self.distribution: str = self.getDistribution()
		# finally call randomWalk()
		self.randomWalk()

	# # # # # #

	def getStart(self) -> List[Tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[0] != "" and key[0][0].isupper():
				types.append(key)
		if not types:
			types = [key for key in self.dict if key[0] != ""]
		return types

	def getStop(self) -> List[Tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[len(key) - 1].endswith((".", "!", "?")):
				types.append(key)
		return types

	# # # # # #

	def filterDict(
		self,
		sample: Iterable[Tuple[str, ...]],
		intersect: bool = True,
	) -> None:
		if intersect:  # keep only these items in dictionary
			# clear the temporary dict
			self.subTokens = 0
			self.subTypes = 0
			self.vocab = {}
			# add matching items to dict
			for phrase in sample:
				self.subTokens += self.dict[phrase]
				self.subTypes += 1
				self.vocab[phrase] = self.dict[phrase]
		else:  # remove items from dictionary
			# create a copy of the whole dict
			self.vocab = self.dict.copy()
			self.subTokens = self.tokens
			self.subTypes = self.types
			# remove items from the dict
			for phrase in sample:
				self.subTokens -= self.vocab[phrase]
				self.subTypes -= 1
				del self.vocab[phrase]

	def filterPhrase(self) -> None:
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

	def randomWordByProb(self) -> Tuple[str, ...]:
		if self.subTokens <= 0:
			raise ValueError("cannot select a word from an empty distribution")

		selection = randrange(self.subTokens)
		for key in self.vocab:
			selection -= self.vocab[key]
			if selection < 0:
				return key
		raise RuntimeError("word counts do not match the distribution total")

	def randomWalk(self) -> None:
		self.filterDict(self.starters)
		# print(f'vocab: {self.vocab}')
		self.subPhrase = self.randomWordByProb()
		sentence = []
		for word in self.subPhrase:
			sentence.append(word)
		self.filterPhrase()
		while self.subPhrase not in self.stoppers:
			self.subPhrase = self.randomWordByProb()
			sentence.append(self.subPhrase[len(self.subPhrase) - 1])
			self.filterPhrase()
			# print(self.vocab)
		self.sentance = " ".join(sentence)

	# # # # # #

	def getDistribution(self) -> str:
		# WARNING: this function is displayed in permille, not percent!!!
		# That means that 1000‰ = 1. Again, 1‰ ≠ 1%!!!
		string = ""
		for key in self.dict:
			value = self.dict[key] / self.tokens * 1000
			string += f"{key}: {value}‰\n"
		return string


if __name__ == "__main__":
	fishy = "One fish two fish red fish blue fish."
	Engine = RandomWalk(fishy, 3)
	print(Engine.distribution)
	print(Engine.sentance)
