import unittest
from unittest.mock import patch

from src.random_walk import RandomWalk


class RandomWalkTest(unittest.TestCase):
	def test_skips_start_phrases_without_a_path_to_sentence_end(self):
		corpus = "Begin. Start middle end. Other tail"

		with patch("src.random_walk.randrange", return_value=0):
			walk = RandomWalk(corpus, 2)

		self.assertNotIn(("Other", "tail"), walk.starters)
		self.assertEqual(walk.sentance, "Begin. Start middle end.")

	def test_generates_a_sentence_and_distribution_from_corpus(self):
		corpus = "One fish two fish red fish blue fish."

		with patch("src.random_walk.randrange", return_value=0):
			walk = RandomWalk(corpus, 3)

		self.assertEqual(walk.sentance, corpus)
		self.assertIn("('One', 'fish', 'two'): ", walk.distribution)
		self.assertIn("‰", walk.distribution)


if __name__ == "__main__":
	unittest.main()
