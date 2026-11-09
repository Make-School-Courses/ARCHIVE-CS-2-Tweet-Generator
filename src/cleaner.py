import re
from pathlib import Path

DATA_DIR: Path = Path(__file__).resolve().parent / "data" / "corpora"


def read_corpus(source: Path) -> str:
	"""Read the input text"""
	with open(source, encoding="utf-8") as file:
		text = file.read()
	return text


def clean_text(text: str) -> str:
	"""Clean the input text"""
	text = re.sub(r"[^a-zA-Z'\-,.!?&]", " ", text)
	words = text.split()
	return " ".join(words)


if __name__ == "__main__":
	source = DATA_DIR / "frankenstein_450.txt"
	text = read_corpus(source)
	text = clean_text(text)
	print(text)

# had some help from my main man, Fang!
# https://github.com/MakeFang/TweetGen/blob/master/Tweet_Generator/tokenization.py
