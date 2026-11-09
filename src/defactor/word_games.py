import random  # Generate random selections.
import re  # Tokenize text with regular expressions.
import urllib.request  # Fetch Project Gutenberg text.
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

from flask import Flask

app: Flask = Flask(__name__)
DATA_EXAMPLE: Path = Path(__file__).resolve().parent.parent / "data" / "example.txt"


def dictionary_main() -> str:
	"""
	Read the system word list from
	`/usr/share/dict/words`.
	"""
	with open("/usr/share/dict/words") as file:
		return file.read()


def publication_random() -> str:
	"""
	Fetch a random Project Gutenberg book
	and return decoded text with line breaks
	normalized to spaces.
	"""
	book = round((random.random() * 49544) + 1)
	link = f"http://www.gutenberg.org/cache/epub/{book}/pg{book}.txt"
	with urllib.request.urlopen(link) as response:
		text = response.read().decode("utf-8")
	print("200 SUCCESS")
	text = text.replace("\r\n", " ")
	text = text.replace("\n", " ")
	text = text.replace("\r", " ")
	return text


def publication_example() -> str:
	"""Read the bundled example text from `DATA_EXAMPLE`."""
	with open(DATA_EXAMPLE) as file:
		return file.read()


def user_number(feed: object) -> int:
	"""
	Prompt until the user enters
	an integer.
	"""
	print(feed)
	while True:
		try:
			return int(input("enter integer:\n>> "))
		except ValueError:
			print("INVALID INPUT.\nplease try again.\n")


def user_string(feed: object) -> str:
	"""Display a prompt and return the user's input."""
	print(feed)
	return input("enter string:\n>> ")


def listify_data(input_data: object) -> List[str]:
	"""
	Split `str(input_data)` on word characters
	and apostrophes.
	"""
	return re.findall(r"[\w']+", str(input_data))


def undupli_list(input_list: List[str]) -> List[str]:
	"""
	Return unique items from `input_list`,
	preserving their original order.
	"""
	return list(dict.fromkeys(input_list))


def randify_list(input_list: List[str], iterations: int) -> List[str]:
	"""
	Randomly remove up to `iterations` items
	from `input_list` and return them.
	This mutates `input_list`. If `iterations`
	is zero, all remaining items are returned.
	"""
	output_list = []
	while input_list and (iterations == 0 or len(output_list) < iterations):
		index = random.randint(0, len(input_list) - 1)
		output_list.append(input_list.pop(index))
	return output_list


def textify_list(input_list: Iterable[str]) -> str:
	"""Join `input_list` with single spaces."""
	return " ".join(input_list)


def textify_dict(input_dict: Dict[str, int]) -> str:
	"""
	Format positive counts as lines, sorted
	from lowest to highest frequency.
	"""
	sorted_items = sorted(
		input_dict.items(),
		key=lambda item: item[1],
	)
	output_lines = []
	for word, count in sorted_items:
		if count > 0:
			output_lines.append(f"{count} {word}\n")
	return "".join(output_lines)


def lowerfy_list(input_list: List[str]) -> List[str]:
	"""
	Return a lowercase copy of `input_list`.
	"""
	return [text.lower() for text in input_list]


def reverse_text(old_word: str) -> str:
	"""
	Return `old_word` with its characters
	in reverse order.
	"""
	return old_word[::-1]


# Word-generation functions
def rearrange(iterations: int, input_data: Optional[object] = None) -> str:
	"""
	Return up to `iterations` random words
	from `input_data`, joined by spaces.
	Zero selects all words.
	"""
	if input_data is None:
		input_data = dictionary_main()
	words = listify_data(input_data)
	words = lowerfy_list(words)
	words = randify_list(words, iterations)
	return textify_list(words)


# Anagrams


def anagrams(
	input_word: str,
	input_data: Optional[object] = None,
) -> str:
	"""
	Return matching lowercase tokens from
	`input_data`, joined by spaces.
	"""
	if input_data is None:
		input_data = dictionary_main()
	words = lowerfy_list(listify_data(input_data))
	matching_words = []
	for word in words:
		if verify_anagram(input_word, word):
			matching_words.append(word)
	return textify_list(matching_words)


def verify_anagram(input_word: str, verify_word: str) -> bool:
	"""
	Check if `input_word` and `verify_word`
	contain the same characters.
	"""
	return sorted(input_word) == sorted(verify_word)


# Palindromes


def palindromes(input_data: Optional[object] = None) -> str:
	"""
	Return unique palindrome tokens from
	`input_data`, joined by spaces.
	"""
	if input_data is None:
		input_data = dictionary_main()
	words = lowerfy_list(listify_data(input_data))
	matches = []
	for word in words:
		if verify_palindrome(word):
			matches.append(word)
	return textify_list(undupli_list(matches))


def verify_palindrome(input_word: str) -> bool:
	"""
	Check if `input_word` reads the same
	forwards and backwards.
	"""
	return input_word == input_word[::-1]


# Histograms


def histogram(input_data: Optional[object] = None) -> Dict[str, int]:
	"""
	Count lowercase word-like tokens and
	return their frequencies.
	"""
	if input_data is None:
		input_data = dictionary_main()
	hist = {}
	for word in lowerfy_list(listify_data(input_data)):
		hist[word] = hist.get(word, 0) + 1
	return hist


def histogram_arrays(
	input_data: Optional[object] = None,
) -> List[List[Union[str, int]]]:
	"""Return mutable `[word, count]` pairs."""
	hist = histogram(input_data)
	rows = []
	for word, count in hist.items():
		rows.append([word, count])
	return rows


def display_dict(input_data: Optional[object] = None) -> str:
	"""
	Format counts from `input_data` as lines,
	sorted by ascending frequency.
	"""
	counts = histogram(input_data)
	return textify_dict(counts)


def display_weight(input_data: Optional[object] = None) -> Optional[str]:
	"""
	Randomly select a token from
	`input_data`, weighted by frequency.
	"""
	counts = histogram(input_data)
	weights = calculate_weight(counts)
	return random_choice(weights)


# Weighted selection


def calculate_weight(input_dict: Dict[str, int]) -> Dict[str, float]:
	"""
	Convert counts in `input_dict` to
	proportions of the total.
	"""
	dict_total = sum(input_dict.values())
	weights = {}
	for word, count in input_dict.items():
		weights[word] = count / dict_total
	return weights


def random_choice(weight_dict: Dict[str, float]) -> Optional[str]:
	"""
	Choose and print a token from
	`weight_dict` by its weight.
	"""
	rand_select = random.random()
	cumulative = 0.0
	for word, weight in weight_dict.items():
		if cumulative <= rand_select < weight + cumulative:
			print("SELECTED: " + word)
			return word
		cumulative += weight
	print(rand_select)


# Flask route


@app.route("/")
def random_gutenberg_word() -> str:
	"""
	Return a random token weighted by its
	frequency in a random Project Gutenberg book.
	"""
	random_pub = publication_random()
	token = display_weight(random_pub)
	if not token:
		raise ValueError("No token was selected.")
	return token


if __name__ == "__main__":
	# Run the random-book word selector from the command line.
	display_weight(publication_random())
