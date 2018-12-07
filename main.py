from random_walk import *
from cleaner import *


if __name__ == '__main__':
	corpus = getCorpus('dnd_phb.txt')
	filter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 .,;!?&"
	cleaned = clean(corpus, filter)
	print("ITS BEEN CLEANED!")
	Walk = RandomWalk(cleaned, 3)
	Walk.randomWalk()