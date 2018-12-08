# send our python in a bottle to the open seas of the web 🌊 (use flask)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def deploy():
	return 'hello'
	source = tuple(['/corpora/sherlock_300.txt'])
	return generate(source, 3)

# import other important files
from cleaner import *
from random_walk import *

# generate a sentance from our corpus at nth order
def generate(corpora, order):
	source = ''
	for work in corpora:
		text = readCorpus(work)
		text = cleanText(text)
		source += text
	Engine = RandomWalk(source, order)
	print(Engine.sentance)
	return Engine.sentance

if __name__ == '__main__':
	source = tuple(['corpora/sherlock_300.txt'])
	generate(source, 3)