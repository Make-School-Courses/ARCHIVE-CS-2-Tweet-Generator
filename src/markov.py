from typing import Dict, List, Tuple


class MarkovChain:
	"""Build an nth-order Markov chain from a corpus."""

	def __init__(self, corpus: str, order: int) -> None:
		if order < 1:
			raise ValueError("Order must be at least 1.")
		# Import arguments.
		self.corpus: str = corpus
		self.order: int = order
		# Initialize empty variables.
		self.word: str = ""
		self.phrase: List[str] = []
		self.dict: Dict[Tuple[str, ...], int] = {}
		self.types: int = 0
		self.tokens: int = 0
		# Build the Markov chain.
		self.save_dict()

	def save_word(self) -> None:
		"""
		Saves a complete word into the phrase, then resets the word.
		Results are saved in self.word.
		---
		When a word is being formed:
		> It is stored in self.word.
		When a word is complete:
		> It is added to self.phrase, then reset.
		"""
		if len(self.phrase) < self.order:
			self.phrase += [self.word]
		if len(self.phrase) == self.order:
			self.save_phrase()
		self.word = ""

	def save_phrase(self) -> None:
		"""
		Saves a complete phrase into the dictionary, then resets it.
		Results are saved in self.phrase.
		---
		When a phrase is being formed:
		> It is stored in self.phrase.
		When a phrase is complete:
		> It is added to self.dict, then reset.
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
		Creates a Markov chain by looping through each letter in the corpus.
		The results are saved in self.dict.
		---
		When a dictionary is being formed:
		> It is stored as a histogram in self.dict.
		When a dictionary is complete:
		> It is added to self.dict.
		"""
		self.dict = {}
		for grapheme in self.corpus:
			if grapheme == " ":  # This can be improved greatly.
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
