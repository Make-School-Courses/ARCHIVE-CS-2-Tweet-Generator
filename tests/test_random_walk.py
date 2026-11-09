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


if __name__ == "__main__":
	unittest.main()
