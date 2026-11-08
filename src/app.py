# send our python in a bottle to the open seas of the web 🌊 (use flask)
from pathlib import Path
from typing import Iterable

from flask import Flask

from .cleaner import cleanText, readCorpus
from .random_walk import RandomWalk
from .twitter import tweet

app: Flask = Flask(__name__)
DATA_DIR: Path = Path(__file__).resolve().parent / "data" / "corpora"


# generate a sentance from our corpus at nth order
def generate(corpora: Iterable[Path], order: int) -> str:
	source = ""
	for work in corpora:
		text = readCorpus(work)
		text = cleanText(text)
		source += text
		source += " "
	Engine = RandomWalk(source, order)
	print(Engine.sentance)
	return Engine.sentance


@app.route("/")
def deploy() -> str:
	source = (DATA_DIR / "frankenstein_450.txt", DATA_DIR / "sherlock_300.txt")
	sentance = generate(source, 3)
	tweet(sentance)
	html = f"""
		<div style="height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center">
			<h1 style="text-align:center; width: 50%; margin:0 auto">{sentance}</h1>
			<hr />
			<p style="text-align: center">
				<em>
					<a href="https://twitter.com/frankensteinen1">
						this message was also tweeted! check it out!
					</a>
				</em>
			</p>
		</div>"""
	return html


if __name__ == "__main__":
	source = (DATA_DIR / "frankenstein_450.txt", DATA_DIR / "sherlock_300.txt")
	generate(source, 3)
