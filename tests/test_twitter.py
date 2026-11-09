import unittest
from unittest.mock import Mock, patch

from src import twitter


class TweetTest(unittest.TestCase):
	@patch("src.twitter.session.post")
	def test_tweet_uses_timeout_and_checks_response(self, post):
		response = Mock()
		response.text = "posted"
		post.return_value = response

		result = twitter.tweet("hello")

		self.assertEqual(result, "posted")
		post.assert_called_once_with(
			twitter.url,
			{"status": "hello"},
			timeout=10,
		)
		response.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
	unittest.main()
