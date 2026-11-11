import os
from dataclasses import dataclass
from datetime import datetime, timezone

import dotenv
import requests

dotenv.load_dotenv(".env")

# Bluesky's XRPC API is used for both session creation and post creation.
api_url = "https://bsky.social/xrpc"
public_api_url = "https://public.api.bsky.app/xrpc"
BLUESKY_HANDLE = "frankensteinengine.bsky.social"


@dataclass(frozen=True)
class BlueskyProfile:
	display_name: str
	handle: str
	avatar_url: str
	is_bot: bool


def get_profile() -> BlueskyProfile:
	"""Load the account's public profile from Bluesky."""
	response = requests.get(
		f"{public_api_url}/app.bsky.actor.getProfile",
		params={"actor": BLUESKY_HANDLE},
		timeout=10,
	)
	response.raise_for_status()
	profile = response.json()
	display_name = profile.get("displayName")
	handle = profile.get("handle")
	avatar_url = profile.get("avatar")
	if not all(
		isinstance(value, str) and value
		for value in (display_name, handle, avatar_url)
	):
		raise ValueError(
			"Bluesky profile is missing its name, handle, or avatar."
		)
	labels = profile.get("labels", [])
	is_bot = isinstance(labels, list) and any(
		isinstance(label, dict) and label.get("val") == "bot"
		for label in labels
	)
	return BlueskyProfile(display_name, handle, avatar_url, is_bot)


def tweet(status: str) -> str:
	"""Post a Bluesky post and return its AT URI."""
	# The handle identifies the account; authenticate with its app password.
	app_password = os.environ.get("BLUESKY_APP_PASSWORD")

	# Raise an error when credentials have not been configured.
	if not app_password:
		raise RuntimeError("Set $BLUESKY_APP_PASSWORD to post to Bluesky.")

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
	return response.json()["uri"]
