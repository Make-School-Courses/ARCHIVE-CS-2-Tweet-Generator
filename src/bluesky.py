import os
from datetime import datetime, timezone

import dotenv
import requests

dotenv.load_dotenv(".env")

# Bluesky's XRPC API is used for both session creation and post creation.
api_url = "https://bsky.social/xrpc"
BLUESKY_HANDLE = "frankensteinengine.bsky.social"


def tweet(status: str) -> str:
	"""Post a tweet as a Bluesky post and return the API response."""
	# The handle identifies the account; authenticate with its app password.
	app_password = os.environ.get("BLUESKY_APP_PASSWORD")

	# Raise an error when credentials have not been configured.
	if not app_password:
		raise RuntimeError(
			"Set $BLUESKY_APP_PASSWORD to post to Bluesky."
		)

	# Create a session to obtain the account DID and access token.
	session = requests.post(
		f"{api_url}/com.atproto.server.createSession",
		json={"identifier": BLUESKY_HANDLE, "password": app_password},
		timeout=10,
	)

	session.raise_for_status()
	auth = session.json()

	# Post a record to Bluesky using the session.
	timeStampNow = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
	response = requests.post(
		f"{api_url}/com.atproto.repo.createRecord",
		json={
			"repo": auth["did"],
			"collection": "app.bsky.feed.post",
			"record": {
				"$type": "app.bsky.feed.post",
				"text": status,
				"createdAt": timeStampNow,
			},
		},
		headers={"Authorization": f"Bearer {auth['accessJwt']}"},
		timeout=10,
	)

	response.raise_for_status()
	return response.text
