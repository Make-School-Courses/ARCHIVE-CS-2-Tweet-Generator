import unittest
from contextlib import redirect_stdout
from io import BytesIO, StringIO
from unittest import TestCase
from unittest.mock import patch

from src.defactor.word_games import calculate_weight, publication_random


class PublicationRandomTest(TestCase):
	def test_decodes_response_and_preserves_line_boundaries(self):
		response = BytesIO("café\r\nsecond\nthird\rfourth".encode())
		output = StringIO()

		with patch(
			"src.defactor.word_games.random.random",
			return_value=0,
		), patch(
			"src.defactor.word_games.urllib.request.urlopen",
			return_value=response,
		), redirect_stdout(output):
			text = publication_random()

		self.assertEqual(text, "café second third fourth")
		self.assertNotIn("b'", text)
		self.assertEqual(output.getvalue(), "200 SUCCESS\n")

	def test_calculate_weight_rejects_nonpositive_total(self):
		for counts in ({}, {"a": 0}, {"a": -1}):
			with self.subTest(counts=counts), self.assertRaisesRegex(
				ValueError,
				"positive total",
			):
				calculate_weight(counts)


if __name__ == "__main__":
	unittest.main()
