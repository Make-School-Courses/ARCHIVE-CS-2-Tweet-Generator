import unittest
from unittest.mock import patch

from src.app import app


class AppTest(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		self.client = app.test_client()

	@patch("src.app.tweet")
	@patch("src.app.generate", return_value="A generated sentence.")
	def test_homepage_shows_generate_button_without_generating_or_posting(
		self,
		generate,
		tweet,
	):
		response = self.client.get("/tweet-generator")

		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Generate a Phrase!", response.data)
		self.assertIn(
			b'action="/tweet-generator/generate"',
			response.data,
		)
		self.assertIn(
			b'<script type="module" src="/static/generate.mjs"></script>',
			response.data,
		)
		generate.assert_not_called()
		tweet.assert_not_called()

	def test_homepage_displays_results_from_query_params(self):
		response = self.client.get(
			"/tweet-generator",
			query_string={
				"phrase": "A generated sentence.",
				"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn(
			b"<p>Phrase: A generated sentence.</p>",
			response.data,
		)
		self.assertIn(
			b"<p>Tweet ID: at://did:plc:alice/app.bsky.feed.post/abc</p>",
			response.data,
		)

	@patch(
		"src.app.tweet",
		return_value="at://did:plc:alice/app.bsky.feed.post/abc",
	)
	@patch("src.app.generate", return_value="A generated sentence.")
	def test_generate_route_returns_json_for_server_generated_phrase(
		self, generate, tweet
	):
		response = self.client.post("/tweet-generator/generate")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")
		expected = {
			"phrase": "A generated sentence.",
			"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
		}
		self.assertEqual(response.json, expected)
		generate.assert_called_once()
		tweet.assert_called_once_with("A generated sentence.")

	@patch(
		"src.app.tweet",
		return_value="at://did:plc:alice/app.bsky.feed.post/abc",
	)
	@patch("src.app.generate", return_value="")
	def test_generate_route_returns_empty_phrase_as_json(self, generate, tweet):
		response = self.client.post("/tweet-generator/generate")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")
		expected = {
			"phrase": "",
			"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
		}
		self.assertEqual(response.json, expected)
		generate.assert_called_once()
		tweet.assert_called_once_with("")


if __name__ == "__main__":
	unittest.main()
