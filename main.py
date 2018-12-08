from cleaner import *
from random_walk import *

def generate(corpora, order):
	source = ''
	for work in corpora:
		text = readCorpus(work)
		text = cleanText(text)
		source += text
	Engine = RandomWalk(source, order)
	print(Engine.sentance)

if __name__ == '__main__':
	source = tuple(['corpora/sherlock_300.txt'])
	generate(source, 3)