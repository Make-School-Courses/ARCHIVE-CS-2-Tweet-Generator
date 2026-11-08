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
	and stringify the response bytes.
	"""
	book = round((random.random() * 49544) + 1)
	link = f"http://www.gutenberg.org/cache/epub/{book}/pg{book}.txt"
	with urllib.request.urlopen(link) as response:
		text = response.read()
	print("200 SUCCESS")
	text = str(text)
	text = text.replace("\\r\\n", "")
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
			number = int(input("enter integer:\n>> "))
			assert isinstance(number, int)
			assert number is not None
			assert number != ""
			return number
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
	input_data = str(input_data)
	if type(input_data) is str:
		input_data = re.findall(r"[\w']+", input_data)
	assert type(input_data) is list
	return input_data


def undupli_list(input_list: List[str]) -> List[str]:
	"""
	Return unique items from `input_list`,
	preserving their original order.
	"""
	output_list = []
	for word in input_list:
		if word not in output_list:
			output_list += [word]
	return output_list


def randify_list(input_list: List[str], iterations: int) -> List[str]:
	"""
	Randomly remove up to `iterations` items
	from `input_list` and return them.
	This mutates `input_list`. If `iterations`
	is zero, all remaining items are returned.
	"""
	output_list = []
	while len(input_list) > 0 and (len(output_list) < iterations or iterations == 0):
		digit_rand = random.randint(0, len(input_list) - 1)
		input_rand = input_list.pop(digit_rand)
		output_list += [input_rand]
	return output_list


def textify_list(input_list: Iterable[str]) -> str:
	"""Join `input_list` with single spaces."""
	output_text = ""
	for input_item in input_list:
		if output_text != "":
			output_text += " "
		output_text += input_item
	input_list = output_text
	return input_list


def textify_dict(input_dict) -> str:
	"""
	Format positive counts as lines, sorted
	from lowest to highest frequency.
	"""
	output_text = ""
	for w in sorted(input_dict, key=input_dict.get, reverse=False):
		if input_dict[w] > 0:
			output_text += str(input_dict[w]) + " " + str(w) + "\n"
	return output_text


def lowerfy_list(input_list: List[str]) -> List[str]:
	"""
	Return a lowercase copy of `input_list`.
	"""
	output_list = []
	for text in input_list:
		output_list += [text.lower()]
	return output_list


def reverse_text(old_word: str) -> str:
	"""
	Return `old_word` with its characters
	in reverse order.
	"""
	new_word = ""
	i = 1
	for _ in old_word:
		new_word += old_word[len(old_word) - i]
		i += 1
	return new_word


# Word-generation functions
def rearrange(iterations: int, input_data: Optional[object] = None) -> str:
	"""
	Return up to `iterations` random words
	from `input_data`, joined by spaces.
	Zero selects all words.
	"""
	if input_data is None:
		input_data = dictionary_main()
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	data = randify_list(data, iterations)
	data = textify_list(data)
	return data


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
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	new_data = []
	i_word = input_word
	for v_word in data:
		if verify_anagram(i_word, v_word):
			new_data += [v_word]
	new_data = textify_list(new_data)
	return new_data


def verify_anagram(input_word: str, verify_word: str) -> bool:
	"""
	Check if `input_word` and `verify_word`
	contain the same characters.
	"""
	input_list = list(input_word)
	verify_list = list(verify_word)
	input_list.sort()
	verify_list.sort()
	return input_list == verify_list


# Palindromes


def palindromes(input_data: Optional[object] = None) -> str:
	"""
	Return unique palindrome tokens from
	`input_data`, joined by spaces.
	"""
	if input_data is None:
		input_data = dictionary_main()
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	new_data = []
	for word in data:
		if verify_palindrome(word):
			new_data += [word]
	new_data = undupli_list(new_data)
	new_data = textify_list(new_data)
	return new_data


def verify_palindrome(input_word: str) -> bool:
	"""
	Check if `input_word` reads the same
	forwards and backwards.
	"""
	i = 1
	while i <= len(input_word) / 2:
		if input_word[i - 1] != input_word[-i]:
			return False
		i += 1
	return True


# Histograms


def histogram(input_data: Optional[object] = None) -> Dict[str, int]:
	"""
	Count lowercase word-like tokens and
	return their frequencies.
	"""
	if input_data is None:
		input_data = dictionary_main()
	data = listify_data(input_data)
	data = lowerfy_list(data)
	hist = {}
	for word in data:
		if word in hist:
			hist[word] += 1
		else:
			hist[word] = 1
	return hist


def histogram_arrays(
	input_data: Optional[object] = None,
) -> List[List[Union[str, int]]]:
	"""Return mutable `[word, count]` pairs."""
	if input_data is None:
		input_data = dictionary_main()
	data = listify_data(input_data)
	data = lowerfy_list(data)
	hist = []

	for word in data:
		for item in hist:
			if word == item[0]:
				item[1] += 1
				break
		else:
			hist.append([word, 1])
	return hist


def display_dict(input_data: Optional[object] = None) -> str:
	"""
	Format counts from `input_data` as lines,
	sorted by ascending frequency.
	"""
	if input_data is None:
		input_data = dictionary_main()
	hist = histogram(input_data)
	output = textify_dict(hist)
	return output


def display_weight(input_data: Optional[object] = None) -> Optional[str]:
	"""
	Randomly select a token from
	`input_data`, weighted by frequency.
	"""
	if input_data is None:
		input_data = dictionary_main()
	hist = histogram(input_data)
	hist = calculate_weight(hist)
	return random_choice(hist)


# Weighted selection


def calculate_weight(input_dict: Dict[str, int]) -> Dict[str, float]:
	"""
	Convert counts in `input_dict` to
	proportions of the total.
	"""
	weight_dict = {}
	dict_total = 0
	for word in input_dict:
		dict_total += input_dict[word]
	for word in input_dict:
		weight_dict[word] = input_dict[word] / dict_total
	return weight_dict


def random_choice(weight_dict: Dict[str, float]) -> Optional[str]:
	"""
	Choose and print a token from
	`weight_dict` by its weight.
	"""
	cumulative = 0
	rand_select = random.random()
	for word in weight_dict:
		if cumulative <= rand_select < weight_dict[word] + cumulative:
			print("SELECTED: " + word)
			return word
		cumulative += weight_dict[word]
	print(rand_select)


# Flask route


@app.route("/")
def hello_world() -> Optional[str]:
	"""
	Return a random token weighted by
	its frequency in a Project Gutenberg book.
	"""
	return display_weight(publication_random())


if __name__ == "__main__":
	# Run the random-book word selector from the command line.
	display_weight(publication_random())
