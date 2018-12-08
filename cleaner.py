import re

def readCorpus(source):
	'''Read the input text'''
	with open(source, 'r') as file:
		text = file.read()
	return text


def cleanText(text):
	'''Clean the input text'''
	text = re.sub("[^a-zA-Z'\-,.!?&]", " ", text)
	text = text.split()
	text = ' '.join(text)
	return text

if __name__ == '__main__':
	# source = 'corpora/dnd_phb.txt'
	source = 'corpora/frankenstein.txt'
	text = readCorpus(source)
	text = cleanText(text)
	print(text)

# had some help from my main man, Fang!
# https://github.com/MakeFang/TweetGen/blob/master/Tweet_Generator/tokenization.py