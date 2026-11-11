import unittest
from unittest.mock import patch

from src.app import app, compress_phrase


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
		self.assertIn(b"<h1>Tweet Generator</h1>", response.data)
		self.assertIn(
			b"Using Markov Chains, this site generates a phrase",
			response.data,
		)
		self.assertIn(b'including "Frankenstein".', response.data)
		self.assertIn(b"Generate a Phrase!", response.data)
		self.assertIn(
			b'href="https://bsky.app/profile/frankensteinengine.bsky.social"',
			response.data,
		)
		self.assertIn(
			b'href="https://github.com/noltron000/tweet-generator"',
			response.data,
		)
		self.assertIn(
			b'action="/tweet-generator/generate"',
			response.data,
		)
		self.assertIn(
			b'src="/tweet-generator/static/generate.mjs"',
			response.data,
		)
		self.assertIn(b'id="loading-status"', response.data)
		self.assertIn(b'aria-live="polite"', response.data)
		self.assertIn(b"Generating tweet...", response.data)
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
			b'<p lang="en">A generated sentence.</p>',
			response.data,
		)
		self.assertIn(b'<section id="generated-result">', response.data)
		self.assertIn(
			b'class="bluesky-embed"',
			response.data,
		)
		self.assertIn(
			b'data-bluesky-uri="at://did:plc:alice/app.bsky.feed.post/abc"',
			response.data,
		)
		self.assertIn(
			b'src="https://embed.bsky.app/static/embed.js"',
			response.data,
		)
		self.assertNotIn(
			b"Tweet ID:",
			response.data,
		)

	def test_homepage_decompresses_phrase_from_query_params(self):
		phrase = "A generated sentence that is long enough to compress. " * 4
		compressed_phrase = compress_phrase(phrase)
		self.assertLess(len(compressed_phrase), len(phrase))
		response = self.client.get(
			"/tweet-generator",
			query_string={
				"compressed_phrase": compressed_phrase,
				"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertIn(
			f'<p lang="en">{phrase}</p>'.encode(),
			response.data,
		)
		self.assertIn(b'class="bluesky-embed"', response.data)

	def test_homepage_rejects_invalid_compressed_phrase(self):
		response = self.client.get(
			"/tweet-generator",
			query_string={"compressed_phrase": "not-valid-deflate"},
		)

		self.assertEqual(response.status_code, 400)

	def test_static_assets_are_served_under_app_path(self):
		response = self.client.get("/tweet-generator/static/style.css")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "text/css")
		response.close()

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
			"compressed_phrase": compress_phrase("A generated sentence."),
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
			"compressed_phrase": compress_phrase(""),
			"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
		}
		self.assertEqual(response.json, expected)
		generate.assert_called_once()
		tweet.assert_called_once_with("")


if __name__ == "__main__":
	unittest.main()
