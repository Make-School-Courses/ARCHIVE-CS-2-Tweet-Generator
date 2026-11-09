import unittest
from contextlib import redirect_stdout
from io import BytesIO, StringIO
from unittest import TestCase
from unittest.mock import patch

from src.defactor.word_games import publication_random


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


if __name__ == "__main__":
	unittest.main()
