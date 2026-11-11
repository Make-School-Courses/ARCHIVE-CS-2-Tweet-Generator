import unittest
from unittest.mock import Mock, patch

from src.app import app, bluesky_post_url, compress_phrase
from src.bluesky import (
	BLUESKY_HANDLE,
	BlueskyProfile,
	get_profile,
	public_api_url,
)


class AppTest(unittest.TestCase):
	def setUp(self):
		app.config["TESTING"] = True
		self.client = app.test_client()

	@patch("src.bluesky.requests.get")
	def test_get_profile_loads_live_profile_fields(self, get):
		response = Mock()
		response.json.return_value = {
			"displayName": "Frankenstein Markov Chain Engine",
			"handle": "frankensteinengine.bsky.social",
			"avatar": "https://cdn.bsky.app/avatar.png",
			"labels": [{"val": "bot"}],
		}
		get.return_value = response

		profile = get_profile()

		self.assertEqual(
			profile,
			BlueskyProfile(
				"Frankenstein Markov Chain Engine",
				"frankensteinengine.bsky.social",
				"https://cdn.bsky.app/avatar.png",
				True,
			),
		)
		get.assert_called_once_with(
			f"{public_api_url}/app.bsky.actor.getProfile",
			params={"actor": BLUESKY_HANDLE},
			timeout=10,
		)
		response.raise_for_status.assert_called_once_with()

	@patch("src.bluesky.requests.get")
	def test_get_profile_rejects_missing_profile_fields(self, get):
		response = Mock()
		response.json.return_value = {
			"handle": "frankensteinengine.bsky.social",
		}
		get.return_value = response

		with self.assertRaisesRegex(
			ValueError,
			"missing its name, handle, or avatar",
		):
			get_profile()

	@patch("src.bluesky.requests.get")
	def test_get_profile_detects_bot_label(self, get):
		response = Mock()
		response.json.return_value = {
			"displayName": "A Person",
			"handle": "person.example",
			"avatar": "https://cdn.bsky.app/avatar.png",
			"labels": [],
		}
		get.return_value = response

		self.assertFalse(get_profile().is_bot)

	@patch("src.app.tweet")
	@patch("src.app.generate", return_value="A generated sentence.")
	def test_homepage_shows_generate_button_without_generating_or_posting(
		self,
		generate,
		tweet,
	):
		response = self.client.get("/tweet-generator")

		self.assertEqual(response.status_code, 200)
		self.assertIn(b"There's a whisper from beyond...", response.data)
		self.assertIn(b"<h1>Tweet Generator</h1>", response.data)
		self.assertIn(
			b"This site generates a random phrase from "
			b"<em>Frankenstein</em> using Markov chains, then posts it "
			b"to Bluesky.",
			response.data,
		)
		self.assertIn(b"Generate a Phrase!", response.data)
		self.assertIn(b'id="generate-form"', response.data)
		self.assertIn(b'class="surface"', response.data)
		for stylesheet in ("theme.css", "layout.css", "components.css"):
			self.assertIn(
				f'href="/tweet-generator/static/{stylesheet}"'.encode(),
				response.data,
			)
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
		self.assertIn(b'id="generate-label"', response.data)
		self.assertIn(b'<span id="loading-status"', response.data)
		generate.assert_not_called()
		tweet.assert_not_called()

	def test_homepage_displays_results_from_query_params(self):
		profile = BlueskyProfile(
			"Loaded Frankenstein",
			"loaded.example",
			"https://cdn.bsky.app/avatar.png",
			True,
		)
		with patch("src.app.get_profile", return_value=profile) as get_profile:
			response = self.client.get(
				"/tweet-generator",
				query_string={
					"phrase": "A generated sentence.",
					"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
				},
			)

		self.assertEqual(response.status_code, 200)
		self.assertIn(b'src="https://cdn.bsky.app/avatar.png"', response.data)
		self.assertIn(b"Loaded Frankenstein", response.data)
		self.assertIn(b"<span>@loaded.example</span>", response.data)
		self.assertIn("🤖".encode(), response.data)
		get_profile.assert_called_once_with()
		self.assertIn(
			b'<p lang="en">A generated sentence.</p>',
			response.data,
		)
		self.assertIn(b'<section id="generated-result">', response.data)
		self.assertIn(
			b'class="surface post-card"',
			response.data,
		)
		self.assertIn(
			b'href="https://bsky.app/profile/did:plc:alice/post/abc"',
			response.data,
		)
		self.assertIn(b'class="bluesky-logo"', response.data)
		self.assertIn(b"View on Bluesky", response.data)
		self.assertNotIn(b"A dispatch from beyond", response.data)
		self.assertNotIn(b"embed.bsky.app", response.data)
		self.assertNotIn(
			b"Tweet ID:",
			response.data,
		)

	def test_homepage_decompresses_phrase_from_query_params(self):
		phrase = "A generated sentence that is long enough to compress. " * 4
		compressed_phrase = compress_phrase(phrase)
		self.assertLess(len(compressed_phrase), len(phrase))
		profile = BlueskyProfile(
			"Loaded Frankenstein",
			"loaded.example",
			"https://cdn.bsky.app/avatar.png",
			True,
		)
		with patch("src.app.get_profile", return_value=profile):
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
		self.assertIn(b'class="surface post-card"', response.data)

	def test_bluesky_post_url_rejects_malformed_uri(self):
		self.assertIsNone(bluesky_post_url("javascript:alert(1)"))

	def test_homepage_rejects_invalid_compressed_phrase(self):
		response = self.client.get(
			"/tweet-generator",
			query_string={"compressed_phrase": "not-valid-deflate"},
		)

		self.assertEqual(response.status_code, 400)

	def test_static_assets_are_served_under_app_path(self):
		for stylesheet, expected in (
			("theme.css", b"--page: #100f10"),
			("layout.css", b"width: min(calc(100% - 2rem), 60rem)"),
			("components.css", b".surface"),
		):
			with self.subTest(stylesheet=stylesheet):
				response = self.client.get(
					f"/tweet-generator/static/{stylesheet}",
				)
				self.assertEqual(response.status_code, 200)
				self.assertEqual(response.mimetype, "text/css")
				self.assertIn(expected, response.data)
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
