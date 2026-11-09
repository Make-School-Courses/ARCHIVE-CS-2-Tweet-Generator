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
		self.sub_types: int = 0
		self.sub_tokens: int = 0
		self.sub_phrase: Tuple[str, ...] = ()
		# call stoppers and starters
		self.stoppers: List[Tuple[str, ...]] = self.get_stop()
		self.starters: List[Tuple[str, ...]] = self.get_start()
		if not self.starters:
			raise ValueError("corpus must contain at least one word")
		if not self.stoppers:
			raise ValueError("corpus must contain sentence-ending punctuation")
		self.distribution: str = self.get_distribution()
		# finally call random_walk()
		self.random_walk()

	# # # # # #

	def get_start(self) -> List[Tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[0] != "" and key[0][0].isupper():
				types.append(key)
		if not types:
			types = [key for key in self.dict if key[0] != ""]
		return types

	def get_stop(self) -> List[Tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[len(key) - 1].endswith((".", "!", "?")):
				types.append(key)
		return types

	# # # # # #

	def filter_dict(
		self,
		sample: Iterable[Tuple[str, ...]],
		intersect: bool = True,
	) -> None:
		if intersect:  # keep only these items in dictionary
			# clear the temporary dict
			self.sub_tokens = 0
			self.sub_types = 0
			self.vocab = {}
			# add matching items to dict
			for phrase in sample:
				self.sub_tokens += self.dict[phrase]
				self.sub_types += 1
				self.vocab[phrase] = self.dict[phrase]
		else:  # remove items from dictionary
			# create a copy of the whole dict
			self.vocab = self.dict.copy()
			self.sub_tokens = self.tokens
			self.sub_types = self.types
			# remove items from the dict
			for phrase in sample:
				self.sub_tokens -= self.vocab[phrase]
				self.sub_types -= 1
				del self.vocab[phrase]

	def filter_phrase(self) -> None:
		self.vocab = self.dict.copy()
		self.sub_tokens = self.tokens
		self.sub_types = self.types
		if self.order > 0:
			for key in self.dict:
				index = self.order - 1
				# print('\n----------')
				# print(f'phs: {self.sub_phrase}')
				# print(f'key: {key}')
				while index > 0:
					if self.sub_phrase[index] != key[index - 1]:
						# print('x')
						self.sub_tokens -= self.vocab[key]
						self.sub_types -= 1
						del self.vocab[key]
						break
					index -= 1

	# # # # # # # # # # # # # # # #
	# def randomWordByCount(self):
	# 	counter = 0
	# 	random = randrange(self.sub_tokens+1)
	# 	for key in self.vocab:
	# 		counter += self.vocab[key]
	# 		if counter >= random:
	# 			return key
	# 	else:
	# 		raise ValueError(f"\ncounter: {counter}  |  random: {random}\nSUMMED COUNTER DIDN'T MEET RANDOM")

	def random_word_by_prob(self) -> Tuple[str, ...]:
		if self.sub_tokens <= 0:
			raise ValueError("cannot select a word from an empty distribution")

		selection = randrange(self.sub_tokens)
		for key in self.vocab:
			selection -= self.vocab[key]
			if selection < 0:
				return key
		raise RuntimeError("word counts do not match the distribution total")

	def random_walk(self) -> None:
		self.filter_dict(self.starters)
		# print(f'vocab: {self.vocab}')
		self.sub_phrase = self.random_word_by_prob()
		sentence = []
		for word in self.sub_phrase:
			sentence.append(word)
		self.filter_phrase()
		while self.sub_phrase not in self.stoppers:
			self.sub_phrase = self.random_word_by_prob()
			sentence.append(self.sub_phrase[len(self.sub_phrase) - 1])
			self.filter_phrase()
			# print(self.vocab)
		self.sentance = " ".join(sentence)

	# # # # # #

	def get_distribution(self) -> str:
		# WARNING: this function is displayed in permille, not percent!!!
		# That means that 1000‰ = 1. Again, 1‰ ≠ 1%!!!
		string = ""
		for key in self.dict:
			value = self.dict[key] / self.tokens * 1000
			string += f"{key}: {value}‰\n"
		return string


if __name__ == "__main__":
	fishy = "One fish two fish red fish blue fish."
	engine = RandomWalk(fishy, 3)
	print(engine.distribution)
	print(engine.sentance)
