import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

from werkzeug.exceptions import BadRequest

from src.app import (
	app,
	bluesky_post_url,
	compress_phrase,
	decompress_phrase,
)
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

	def test_homepage_renders_without_loading_a_profile(self):
		with patch("src.app.get_profile") as get_profile:
			response = self.client.get("/tweet-generator")

		self.assertEqual(response.status_code, 200)
		get_profile.assert_not_called()
		self.assertIn(
			'<section id="generated-result" hidden>',
			response.get_data(as_text=True),
		)

	def test_homepage_shows_generated_result_when_phrase_is_present(self):
		response = self.client.get(
			"/tweet-generator",
			query_string={"phrase": "A generated sentence."},
		)
		page = response.get_data(as_text=True)

		self.assertIn('<section id="generated-result">', page)
		self.assertIn("<p>Phrase: A generated sentence.</p>", page)

	def test_homepage_renders_hidden_generation_error_with_issue_link(self):
		response = self.client.get("/tweet-generator")
		page = response.get_data(as_text=True)

		self.assertIn('id="generation-error"', page)
		self.assertIn('role="alert"', page)
		self.assertIn(
			'href="https://github.com/noltron000/tweet-generator/issues/new"',
			page,
		)
		self.assertIn("Report this issue on GitHub", page)

	def test_homepage_decodes_compressed_phrase_before_rendering(self):
		phrase = "A generated sentence with punctuation: caf\u00e9!"
		compressed_phrase = compress_phrase(phrase)
		profile = BlueskyProfile(
			"Loaded Frankenstein",
			"loaded.example",
			"https://cdn.bsky.app/avatar.png",
			True,
		)
		with (
			patch("src.app.get_profile", return_value=profile) as get_profile,
			patch(
				"src.app.render_page",
				return_value="rendered",
			) as render_page,
		):
			response = self.client.get(
				"/tweet-generator",
				query_string={
					"compressed_phrase": compressed_phrase,
					"tweet_id": "at://did:plc:alice/app.bsky.feed.post/abc",
				},
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_data(as_text=True), "rendered")
		get_profile.assert_called_once_with()
		render_page.assert_called_once_with(
			phrase=phrase,
			tweet_id="at://did:plc:alice/app.bsky.feed.post/abc",
			profile=profile,
			post_url="https://bsky.app/profile/did:plc:alice/post/abc",
		)

	def test_homepage_does_not_load_profile_for_invalid_post_uri(self):
		with (
			patch("src.app.get_profile") as get_profile,
			patch("src.app.render_page", return_value="rendered"),
		):
			response = self.client.get(
				"/tweet-generator",
				query_string={
					"phrase": "phrase",
					"tweet_id": "javascript:alert(1)",
				},
			)

		self.assertEqual(response.status_code, 200)
		get_profile.assert_not_called()

	def test_homepage_rejects_invalid_compressed_phrase(self):
		response = self.client.get(
			"/tweet-generator",
			query_string={"compressed_phrase": "not-valid-deflate"},
		)

		self.assertEqual(response.status_code, 400)

	def test_generate_route_returns_phrase_post_uri_and_compressed_phrase(self):
		phrase = "A generated sentence."
		post_uri = "at://did:plc:alice/app.bsky.feed.post/abc"
		with (
			patch("src.app.generate", return_value=phrase) as generate,
			patch("src.app.tweet", return_value=post_uri) as tweet,
		):
			response = self.client.post("/tweet-generator/generate")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, "application/json")
		payload = response.get_json()
		if not isinstance(payload, dict):
			self.fail("Generation route did not return a JSON object.")
		self.assertEqual(payload["phrase"], phrase)
		self.assertEqual(payload["tweet_id"], post_uri)
		self.assertEqual(
			decompress_phrase(payload["compressed_phrase"]),
			phrase,
		)
		generate.assert_called_once()
		tweet.assert_called_once_with(phrase)

	def test_routes_with_trailing_slashes_redirect_to_canonical_routes(self):
		homepage_response = self.client.get(
			"/tweet-generator/",
			query_string={"phrase": "generated"},
		)
		self.assertEqual(homepage_response.status_code, 308)
		homepage_location = urlsplit(
			homepage_response.headers["Location"],
		)
		self.assertEqual(homepage_location.path, "/tweet-generator")
		self.assertEqual(homepage_location.query, "phrase=generated")

		with (
			patch("src.app.generate", return_value="A generated sentence."),
			patch(
				"src.app.tweet",
				return_value="at://did:plc:alice/app.bsky.feed.post/abc",
			),
		):
			generate_response = self.client.post(
				"/tweet-generator/generate/",
			)

		self.assertEqual(generate_response.status_code, 308)
		self.assertEqual(
			urlsplit(generate_response.headers["Location"]).path,
			"/tweet-generator/generate",
		)

	def test_phrase_compression_round_trips_unicode(self):
		phrase = "A whisper from beyond... caf\u00e9 \U0001f47b"
		compressed = compress_phrase(phrase)

		self.assertEqual(decompress_phrase(compressed), phrase)
		self.assertRegex(compressed, r"^[A-Za-z0-9_-]+$")

	def test_decompress_phrase_rejects_expansion_over_limit(self):
		oversized = compress_phrase("a" * 4097)
		with self.assertRaises(BadRequest):
			decompress_phrase(oversized)

	def test_bluesky_post_url_maps_valid_at_uri_and_rejects_invalid_uri(self):
		post_uri = (
			"at://did:plc:ork7vyqfg2a4t4hk5iyp7lxr/"
			"app.bsky.feed.post/3mzyysy7i762c"
		)

		self.assertEqual(
			bluesky_post_url(post_uri),
			"https://bsky.app/profile/"
			"did:plc:ork7vyqfg2a4t4hk5iyp7lxr/post/3mzyysy7i762c",
		)
		self.assertIsNone(bluesky_post_url("javascript:alert(1)"))

	@patch("src.bluesky.requests.get")
	def test_get_profile_loads_account_fields_and_bot_label(self, get):
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
	def test_get_profile_rejects_missing_required_fields(self, get):
		response = Mock()
		response.json.return_value = {"handle": "incomplete.example"}
		get.return_value = response

		with self.assertRaises(ValueError):
			get_profile()


if __name__ == "__main__":
	unittest.main()
