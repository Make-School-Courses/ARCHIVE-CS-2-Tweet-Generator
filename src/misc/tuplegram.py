#!python


class Tuplegram(list):
	"""
	Tuplegram is a histogram implemented as a subclass of the list type.
	"""

	def __init__(self, word_list=None):
		"""
		Initialize this histogram as a new list and count given words.
		"""
		super().__init__()  # Initialize this as a new list
		# Add properties to track useful word counts for this histogram
		self.types = 0  # Count of distinct word types in this histogram
		self.tokens = 0  # Total count of all word tokens in this histogram
		# Count words in given list, if any
		print("SELF:")
		print(self)
		print(word_list)
		if word_list is not None:
			for word in word_list:
				self.add_count(word)

	def add_count(self, word, count=1):
		"""
		Increase frequency count of given word by given count amount.
		"""
		# TODO: Increase word frequency by count
		self.tokens += count
		for item in self:
			if item[0] == word:
				newItem = (item[0], item[1] + count)
				self.remove(item)
				self.append(newItem)
				break
		else:
			self.types += 1
			self.append((word, count))

	def frequency(self, word):
		"""
		Return frequency count of given word, or 0 if word is not found.
		"""
		# Retrieve word frequency count
		for pairing in self:
			if pairing[0] == word:
				return pairing[1]
		return 0

	def __contains__(self, word):
		"""
		Return boolean indicating if given word is in this histogram.
		"""
		# Check if word is in this histogram
		return any(pairing[0] == word for pairing in self)

	def _index(self, word):
		"""
		Return the index of entry containing given word if found
		in this histogram, or None if given word is not found.
		"""
		# Implement linear search to find index of entry with given word
		for index, pairing in enumerate(self):
			if pairing[0] == word:
				return index
		return None


def print_histogram(word_list):
	print(f"word list: {word_list}")
	# Create a tuplegram and display its contents
	histogram = Tuplegram(word_list)
	print(f"tuplegram: {histogram}")
	print(f"{histogram.tokens} tokens, {histogram.types} types")
	for array in histogram:
		word = array[0]
		freq = array[1]
		print(f"{word!r} occurs {freq} times")
	print()


def main():
	import sys

	arguments = sys.argv[1:]  # Exclude script name in first argument
	if len(arguments) >= 1:
		# Test histogram on given arguments
		print_histogram(arguments)
	else:
		# Test histogram on letters in a word
		word = "abracadabra"
		print_histogram(list(word))
		# Test histogram on words in a classic book title
		fish_text = "one fish two fish red fish blue fish"
		print_histogram(fish_text.split())
		# Test histogram on words in a long repetitive sentence
		woodchuck_text = (
			"how much wood would a wood chuck chuck\nif a wood chuck could chuck wood"
		)
		print_histogram(woodchuck_text.split())


if __name__ == "__main__":
	main()
