"""Serve Markov-generated sentences and post them to Twitter."""

from pathlib import Path
from typing import Iterable

from flask import Flask, abort, render_template_string, request

from .cleaner import clean_text, read_corpus
from .random_walk import RandomWalk
from .twitter import tweet

# Send our Python in a bottle to the open seas of the web (use Flask).
app: Flask = Flask(__name__)
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


@app.route("/")
def deploy() -> str:
	"""
	Render a generated sentence for the home page.

	This route combines a few built-in source texts, generates a new sentence,
	and returns the HTML page that presents it to the user.
	"""
	source = (
		DATA_DIR / "frankenstein_450.txt",
		DATA_DIR / "sherlock_300.txt",
	)
	sentance = generate(source, 3)
	return render_page(sentance)


@app.route("/tweet", methods=["POST"])
def post_tweet() -> str:
	sentance = request.form.get("status")
	if not sentance:
		abort(400)
	tweet(sentance)
	return render_page(sentance, tweeted=True)


def render_page(sentance: str, tweeted: bool = False) -> str:
	return render_template_string(
		"""
		<div
			style="height:100%;
			display:flex;
			flex-direction:column;
			align-items:center;
			justify-content:center"
		>
			<h1
				style="text-align:center;
				width:50%;
				margin:0 auto"
			>
				{{ sentance }}
			</h1>
			<hr />

			{% if tweeted %}
				<p style="text-align:center">
					<em>
						<a href="https://twitter.com/frankensteinen1">
							This message was tweeted! Check it out!
						</a>
					</em>
				</p>
			{% else %}
				<form action="/tweet" method="post">
					<input type="hidden" name="status" value="{{ sentance }}">
					<button type="submit">Tweet This!</button>
				</form>
			{% endif %}
		</div>
		""",
		sentance=sentance,
		tweeted=tweeted,
	)
