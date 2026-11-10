"""Serve Markov-generated sentences and post them to Bluesky."""

from collections.abc import Iterable
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request

from .bluesky import tweet
from .cleaner import clean_text, read_corpus
from .random_walk import RandomWalk

# Send our Python in a bottle to the open seas of the web (use Flask).
app: Flask = Flask(__name__, static_folder="static")
DATA_DIR: Path = Path(__file__).resolve().parent / "data" / "corpora"


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
	return render_page(
		phrase=request.args.get("phrase"),
		tweet_id=request.args.get("tweet_id"),
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
		"tweet_id": tweet_id,
	})


def render_page(
	phrase: str | None = None,
	tweet_id: str | None = None,
) -> str:
	"""Render the page with a button for generating and posting a phrase."""
	return render_template(
		"index.jinja",
		phrase=phrase,
		tweet_id=tweet_id,
	)
