import unittest
from unittest.mock import patch

from src.app import app


class AppTest(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		self.client = app.test_client()

	@patch("src.app.tweet")
	@patch("src.app.generate", return_value="A generated sentence.")
	def test_homepage_displays_tweet_button_without_posting(
		self,
		generate,
		tweet,
	):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertIn(b"A generated sentence.", response.data)
		self.assertIn(b"Tweet This!", response.data)
		generate.assert_called_once()
		tweet.assert_not_called()

	@patch("src.app.tweet")
	def test_homepage_generates_from_bundled_corpora(self, tweet):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertIn(b"<h1", response.data)
		self.assertIn(b"Tweet This!", response.data)
		tweet.assert_not_called()

	@patch("src.app.tweet")
	def test_tweet_button_posts_sentence_and_hides_button(self, tweet):
		response = self.client.post(
			"/tweet",
			data={"status": "A generated sentence."},
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn(b"This message was tweeted!", response.data)
		self.assertNotIn(b"Tweet This!", response.data)
		tweet.assert_called_once_with("A generated sentence.")

	@patch("src.app.tweet")
	def test_tweet_requires_a_status(self, tweet):
		response = self.client.post("/tweet")

		self.assertEqual(response.status_code, 400)
		tweet.assert_not_called()


if __name__ == "__main__":
	unittest.main()
