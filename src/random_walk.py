from collections.abc import Iterable
from random import randrange

from .markov import MarkovChain


class RandomWalk(MarkovChain):
	"""Generate a sentence by sampling paths through a Markov chain."""

	def __init__(self, corpus: str, order: int) -> None:
		# Initialize the Markov chain. ⛓
		MarkovChain.__init__(self, corpus, order)
		# Initialize empty variables.
		self.sentance: str = ""
		self.vocab: dict[tuple[str, ...], int] = {}
		self.sub_types: int = 0
		self.sub_tokens: int = 0
		self.sub_phrase: tuple[str, ...] = ()
		# Find sentence endings and starting phrases.
		self.stoppers: list[tuple[str, ...]] = self.get_stop()
		if not self.stoppers:
			raise ValueError(
				"The corpus must contain sentence-ending punctuation."
			)
		self.viable: set[tuple[str, ...]] = self.get_viable()
		self.starters: list[tuple[str, ...]] = [
			phrase for phrase in self.get_start() if phrase in self.viable
		]
		if not self.starters:
			raise ValueError(
				"The corpus must contain a path to a sentence ending."
			)
		self.distribution: str = self.get_distribution()
		# Generate a random walk.
		self.random_walk()

	def get_start(self) -> list[tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[0] != "" and key[0][0].isupper():
				types.append(key)
		if not types:
			types = [key for key in self.dict if key[0] != ""]
		return types

	def get_stop(self) -> list[tuple[str, ...]]:
		types = []
		for key in self.dict:
			if key[len(key) - 1].endswith((".", "!", "?")):
				types.append(key)
		return types

	def get_viable(self) -> set[tuple[str, ...]]:
		prefixes = {}
		predecessors = {phrase: [] for phrase in self.dict}
		for phrase in self.dict:
			prefixes.setdefault(phrase[:-1], []).append(phrase)
		for phrase in self.dict:
			for successor in prefixes.get(phrase[1:], []):
				predecessors[successor].append(phrase)

		viable = set(self.stoppers)
		pending = list(viable)
		while pending:
			for phrase in predecessors[pending.pop()]:
				if phrase not in viable:
					viable.add(phrase)
					pending.append(phrase)
		return viable

	def filter_dict(
		self,
		sample: Iterable[tuple[str, ...]],
		intersect: bool = True,
	) -> None:
		"""Build a sampling distribution from selected or excluded items."""
		if intersect:  # Keep only the selected items.
			# Clear the temporary dictionary.
			self.sub_tokens = 0
			self.sub_types = 0
			self.vocab = {}
			# Add matching items to the dictionary.
			for phrase in sample:
				self.sub_tokens += self.dict[phrase]
				self.sub_types += 1
				self.vocab[phrase] = self.dict[phrase]
		else:  # Remove the selected items.
			# Copy the full dictionary.
			self.vocab = self.dict.copy()
			self.sub_tokens = self.tokens
			self.sub_types = self.types
			# Remove matching items from the copy.
			for phrase in sample:
				self.sub_tokens -= self.vocab[phrase]
				self.sub_types -= 1
				del self.vocab[phrase]

	def filter_phrase(self) -> None:
		"""Keep viable phrases that continue the current state."""
		self.vocab = self.dict.copy()
		self.sub_tokens = self.tokens
		self.sub_types = self.types
		if self.order > 0:
			for key in self.dict:
				if key not in self.viable:
					self.sub_tokens -= self.vocab[key]
					self.sub_types -= 1
					del self.vocab[key]
					continue
				index = self.order - 1
				while index > 0:
					if self.sub_phrase[index] != key[index - 1]:
						self.sub_tokens -= self.vocab[key]
						self.sub_types -= 1
						del self.vocab[key]
						break
					index -= 1

	def random_word_by_prob(self) -> tuple[str, ...]:
		if self.sub_tokens <= 0:
			raise ValueError("Cannot select a word from an empty distribution.")

		selection = randrange(self.sub_tokens)
		for key in self.vocab:
			selection -= self.vocab[key]
			if selection < 0:
				return key
		raise RuntimeError("Word counts do not match the distribution total.")

	def random_walk(self) -> None:
		self.filter_dict(self.starters)
		self.sub_phrase = self.random_word_by_prob()
		sentence = []
		for word in self.sub_phrase:
			sentence.append(word)
		self.filter_phrase()
		while self.sub_phrase not in self.stoppers:
			self.sub_phrase = self.random_word_by_prob()
			sentence.append(self.sub_phrase[-1])
			self.filter_phrase()
		self.sentance = " ".join(sentence)

	def get_distribution(self) -> str:
		"""Return phrase frequencies in per mille (1000‰ equals 1)."""
		# WARNING: this function is displayed in permille, not percent!!!
		# That means that 1000‰ = 1. Again, 1‰ ≠ 1%!!!
		string = ""
		for key in self.dict:
			value = self.dict[key] / self.tokens * 1000
			string += f"{key}: {value}‰\n"
		return string
