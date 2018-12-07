class Markov(object):
	def __init__(self, corpus, order):
		self.corpus = corpus
		self.order = order

		self.dict = {}
		self.phrase = []
		self.word = ''

		self.create()
		print(self.dict)

	def create(self):
		for grapheme in self.corpus:
			if grapheme == ' ': # this can be improved greatly
				self.saveWord()
			else:
				self.word += grapheme
		self.saveWord()

	def saveWord(self):
		if len(self.phrase)  < self.order:
			self.phrase += [self.word]
		if len(self.phrase) == self.order:
			self.savePhrase()
		self.word = ''

	def savePhrase(self):
		phrase = tuple(self.phrase)
		if phrase in self.dict:
			self.dict[phrase] += 1
		else:
			self.dict[phrase]  = 1
		del self.phrase[0]

if __name__ == '__main__':
	fishy = "one fish two fish red fish blue fish"
	model = Markov(fishy, 5)