import unittest

from src.markov import MarkovChain


class MarkovChainTest(unittest.TestCase):
	def test_rejects_nonpositive_order(self):
		for order in (0, -1):
			with (
				self.subTest(order=order),
				self.assertRaisesRegex(
					ValueError,
					"at least 1",
				),
			):
				MarkovChain("one two", order)

	def test_accepts_positive_order(self):
		chain = MarkovChain("one two", 1)

		self.assertEqual(chain.order, 1)
		self.assertTrue(chain.dict)

	def test_counts_phrase_types_and_tokens(self):
		chain = MarkovChain("One fish two fish, red fish blue fish", 1)

		self.assertEqual(chain.dict[("fish",)], 3)
		self.assertEqual(chain.dict[("fish,",)], 1)
		self.assertEqual(chain.types, 6)
		self.assertEqual(chain.tokens, 8)


if __name__ == "__main__":
	unittest.main()
