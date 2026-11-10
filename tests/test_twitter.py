import unittest
from unittest.mock import Mock, patch

from src import twitter


class TweetTest(unittest.TestCase):
	@patch.dict(
		"src.twitter.os.environ",
		{"BLUESKY_APP_PASSWORD": "app-password"},
	)
	@patch("src.twitter.requests.post")
	def test_tweet_creates_session_and_posts_to_bluesky(self, post):
		session_response = Mock()
		session_response.json.return_value = {
			"accessJwt": "access-token",
			"did": "did:plc:alice",
		}
		post_response = Mock()
		post_response.text = "posted"
		post.side_effect = [session_response, post_response]

		result = twitter.tweet("hello")

		self.assertEqual(result, "posted")
		self.assertEqual(post.call_count, 2)
		session_call, record_call = post.call_args_list
		self.assertEqual(
			session_call.args,
			(f"{twitter.api_url}/com.atproto.server.createSession",),
		)
		self.assertEqual(
			session_call.kwargs,
			{
				"json": {
					"identifier": twitter.BLUESKY_HANDLE,
					"password": "app-password",
				},
				"timeout": 10,
			},
		)
		self.assertEqual(
			record_call.args,
			(f"{twitter.api_url}/com.atproto.repo.createRecord"),
		)
		self.assertEqual(
			record_call.kwargs["json"]["repo"],
			"did:plc:alice",
		)
		self.assertEqual(
			record_call.kwargs["json"]["record"]["text"],
			"hello",
		)
		self.assertEqual(
			record_call.kwargs["headers"],
			{"Authorization": "Bearer access-token"},
		)
		session_response.raise_for_status.assert_called_once_with()
		post_response.raise_for_status.assert_called_once_with()

	@patch.dict("src.twitter.os.environ", {}, clear=True)
	@patch("src.twitter.requests.post")
	def test_tweet_requires_bluesky_credentials(self, post):
		with self.assertRaisesRegex(RuntimeError, "BLUESKY_APP_PASSWORD"):
			twitter.tweet("hello")

		post.assert_not_called()


if __name__ == "__main__":
	unittest.main()
