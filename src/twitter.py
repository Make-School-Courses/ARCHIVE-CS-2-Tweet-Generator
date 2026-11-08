import os
from typing import Optional

import dotenv
from requests_oauthlib import OAuth1Session

dotenv.load_dotenv(".env")

consumer_key: Optional[str] = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret: Optional[str] = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token: Optional[str] = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret: Optional[str] = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

session: OAuth1Session = OAuth1Session(
	consumer_key,
	client_secret=consumer_secret,
	resource_owner_key=access_token,
	resource_owner_secret=access_token_secret,
)

# The URL endpoint to update a status (i.e. tweet)
url = "https://api.twitter.com/1.1/statuses/update.json"


def tweet(status: str) -> str:
	print("tweet tweet!")
	resp = session.post(url, {"status": status})
	return resp.text
