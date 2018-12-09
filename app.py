# send our python in a bottle to the open seas of the web 🌊 (use flask)
from flask import Flask
from twitter import *
app = Flask(__name__)

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

@app.route('/')
def deploy():
	fishy = "One fish two fish, red fish blue fish"
	source = tuple(['corpora/frankenstein_450.txt'])
	sentance = generate(source, 3)
	##### CANNOT GET WEB-POSTED TWEETS TO WORK
	# tweet(sentance)
	html = f'''
		<div style="height:100%; display:flex; align-items:center; justify-content:center; max-width:50%">
			<h1>{sentance}</h1>
			<hr />
		</div>'''
	##### CANNOT GET WEB-POSTED TWEETS TO WORK
	# <p style="text-align: center"><em>
	# 	<a href="https://twitter.com/frankensteinen1">
	# 		this message was also tweeted! check it out!
	# 	</a>
	# </p></em>
	return html

# @app.route('/tweet', methods=['POST'])
# def tweet():
# 	status = request.form['sentence']
# 	tweet(status)
# 	return redirect('/')

if __name__ == '__main__':
	source = tuple(['corpora/frankenstein_450.txt'])
	generate(source, 3)