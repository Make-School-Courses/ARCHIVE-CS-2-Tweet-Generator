from cleaner import *
from markov import *

def generate(source, order):
	text = readCorpus(source)
	text = cleanText(text)
	Model = Markov(text, order)


	print(Model.dict)

if __name__ == '__main__':
	# source = 'corpora/dnd_phb.txt'
	source = 'corpora/frankenstein.txt'
	generate(source, 5)