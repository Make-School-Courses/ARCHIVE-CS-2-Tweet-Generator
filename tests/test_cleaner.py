import tempfile
import unittest
from pathlib import Path

from src.cleaner import clean_text, read_corpus


class CleanerTest(unittest.TestCase):
	def test_reads_utf8_corpus(self):
		with tempfile.TemporaryDirectory() as directory:
			source = Path(directory) / "corpus.txt"
			source.write_text("Hello, world!", encoding="utf-8")

			self.assertEqual(read_corpus(source), "Hello, world!")

	def test_removes_unsupported_characters_and_normalizes_whitespace(self):
		text = "Hello,\tworld!  It's 2024 & still-going."

		self.assertEqual(clean_text(text), "Hello, world! It's & still-going.")


if __name__ == "__main__":
	unittest.main()
