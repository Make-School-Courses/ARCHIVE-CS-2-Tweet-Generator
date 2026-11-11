"""Serve Markov-generated sentences and post them to Bluesky."""

import base64
import binascii
import re
import zlib
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import quote

from flask import Flask, Response, abort, jsonify, render_template, request

from .bluesky import BlueskyProfile, get_profile, tweet
from .cleaner import clean_text, read_corpus
from .random_walk import RandomWalk

# Send our Python in a bottle to the open seas of the web (use Flask).
app: Flask = Flask(
	__name__,
	static_folder="static",
	static_url_path="/tweet-generator/static",
)
DATA_DIR: Path = Path(__file__).resolve().parent / "data" / "corpora"
MAX_PHRASE_LENGTH = 4096


def compress_phrase(phrase: str) -> str:
	"""Compress a phrase into URL-safe base64-encoded DEFLATE data."""
	compressor = zlib.compressobj(wbits=-zlib.MAX_WBITS)
	compressed = compressor.compress(phrase.encode("utf-8"))
	compressed += compressor.flush()
	return base64.urlsafe_b64encode(compressed).decode("ascii").rstrip("=")


def decompress_phrase(value: str) -> str:
	"""Decode a compressed phrase from a query parameter."""
	if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
		abort(400, description="Invalid compressed phrase.")
	try:
		padding = "=" * (-len(value) % 4)
		compressed = base64.b64decode(
			value + padding,
			altchars=b"-_",
			validate=True,
		)
		decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
		phrase = decompressor.decompress(compressed, MAX_PHRASE_LENGTH + 1)
		if (
			len(phrase) > MAX_PHRASE_LENGTH
			or decompressor.unconsumed_tail
			or not decompressor.eof
			or decompressor.unused_data
		):
			abort(400, description="Invalid compressed phrase.")
		return phrase.decode("utf-8")
	except (binascii.Error, UnicodeDecodeError, zlib.error):
		abort(400, description="Invalid compressed phrase.")


def bluesky_post_url(uri: str | None) -> str | None:
	"""Convert a Bluesky post AT URI to its public web URL."""
	if uri is None:
		return None
	match = re.fullmatch(
		r"at://([^/?#]+)/app\.bsky\.feed\.post/([^/?#]+)",
		uri,
	)
	if match is None:
		return None
	repo, record_key = match.groups()
	return (
		f"https://bsky.app/profile/{quote(repo, safe=':')}"
		f"/post/{quote(record_key, safe='')}"
	)


def generate(corpora: Iterable[Path], order: int) -> str:
	"""
	Generate a sentence from one or more source corpora.

	The corpus files are read and cleaned, then combined into a single text
	source before building a Markov-style sentence using the configured order.
	"""
	source = ""
	for work in corpora:
		text = read_corpus(work)
		text = clean_text(text)
		source += text
		source += " "
	engine = RandomWalk(source, order)
	print(engine.sentance)
	return engine.sentance


@app.route("/tweet-generator")
def deploy() -> str:
	"""Render the tweet generator homepage."""
	compressed_phrase = request.args.get("compressed_phrase")
	phrase = request.args.get("phrase")
	if compressed_phrase is not None:
		phrase = decompress_phrase(compressed_phrase)
	tweet_id = request.args.get("tweet_id")
	post_url = bluesky_post_url(tweet_id)
	profile = (
		get_profile()
		if post_url is not None and phrase is not None
		else None
	)
	return render_page(
		phrase=phrase,
		tweet_id=tweet_id,
		profile=profile,
		post_url=post_url,
	)


@app.route("/tweet-generator/generate", methods=["POST"])
def generate_and_post() -> Response:
	"""Generates a phrase, posts it to Bluesky, and returns data."""
	# Use this corpora as the booksource.
	source = (
		DATA_DIR / "frankenstein_450.txt",
		DATA_DIR / "sherlock_300.txt",
	)

	# Generate the phrase and tweet.
	phrase = generate(source, 3)
	tweet_id = tweet(phrase)
	return jsonify({
		"phrase": phrase,
		"compressed_phrase": compress_phrase(phrase),
		"tweet_id": tweet_id,
	})


def render_page(
	phrase: str | None = None,
	tweet_id: str | None = None,
	profile: BlueskyProfile | None = None,
	post_url: str | None = None,
) -> str:
	"""Render the page with a button for generating and posting a phrase."""
	return render_template(
		"index.jinja",
		phrase=phrase,
		tweet_id=tweet_id,
		profile=profile,
		post_url=post_url,
	)
