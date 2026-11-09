"""
This file is feature complete.
The class outputs a Markov Chain of nth order, with inputs of corpus and order.
"""

from typing import Dict, List, Tuple


class MarkovChain:
	def __init__(self, corpus: str, order: int) -> None:
		# import arguments
		self.corpus: str = corpus
		self.order: int = order
		# initialize 'empty' variables
		self.word: str = ""
		self.phrase: List[str] = []
		self.dict: Dict[Tuple[str, ...], int] = {}
		self.types: int = 0
		self.tokens: int = 0
		# call save_dict
		self.save_dict()

	def save_word(self) -> None:
		"""
		Saves a complete stored word into the phrase, then resets the stored word.
		The results are saved in self.word
		---
		When a word is being formed:
		> its stored in a string in self.word
		When a word is complete:
		> its put into the self.phrase array, then reset.
		"""
		if len(self.phrase) < self.order:
			self.phrase += [self.word]
		if len(self.phrase) == self.order:
			self.save_phrase()
		self.word = ""

	def save_phrase(self) -> None:
		"""
		Saves a complete stored phrase into the dictionary, then resets the stored phrase.
		The results are saved in self.phrase
		---
		When a phrase is being formed:
		> its stored in an array in self.phrase
		When a phrase is complete:
		> its put into the self.dict dictionary, then reset.
		"""
		phrase = tuple(self.phrase)
		if phrase in self.dict:
			self.dict[phrase] += 1
		else:
			self.dict[phrase] = 1
			self.types += 1
		self.tokens += 1
		del self.phrase[0]

	def save_dict(self) -> None:
		"""
		Creates a markov chain by looping through each letter in the corpus.
		The results are saved in self.dict
		---
		When a dictionary is being formed:
		> its stored in a histogram in self.dict
		When a dictionary is complete:
		> its put into the self.dict dictionary.
		"""
		self.dict = {}
		for grapheme in self.corpus:
			if grapheme == " ":  # this can be improved greatly
				self.save_word()
			else:
				self.word += grapheme
		self.save_word()


if __name__ == "__main__":
	fishy = "One fish two fish, red fish blue fish"
	model = MarkovChain(fishy, 1)
	print(f"DICTIONARY:\n{model.dict}\n")
	print(f"UNIQUE TYPES: {model.types}\n")
	print(f"TOTAL TOKENS: {model.tokens}\n")
