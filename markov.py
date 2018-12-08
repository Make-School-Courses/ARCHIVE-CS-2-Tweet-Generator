'''
	This file is feature complete.
	The class outputs a Markov Chain of nth order, with inputs of corpus and order.
'''

class MarkovChain():
	def __init__(self, corpus, order):
		# import arguments
		self.corpus = corpus
		self.order = order
		# initialize 'empty' variables
		self.word = ''
		self.phrase = []
		self.dict = {}
		self.types = 0
		self.tokens = 0
		# call saveDict
		self.saveDict()

	def saveWord(self):
		'''
			Saves a complete stored word into the phrase, then resets the stored word.
			The results are saved in self.word
			---
			When a word is being formed:
			> its stored in a string in self.word
			When a word is complete:
			> its put into the self.phrase array, then reset.
		'''
		if len(self.phrase)  < self.order:
			self.phrase += [self.word]
		if len(self.phrase) == self.order:
			self.savePhrase()
		self.word = ''

	def savePhrase(self):
		'''
			Saves a complete stored phrase into the dictionary, then resets the stored phrase.
			The results are saved in self.phrase
			---
			When a phrase is being formed:
			> its stored in an array in self.phrase
			When a phrase is complete:
			> its put into the self.dict dictionary, then reset.
		'''
		phrase = tuple(self.phrase)
		if phrase in self.dict:
			self.dict[phrase] += 1
		else:
			self.dict[phrase]  = 1
			self.types += 1
		self.tokens  += 1
		del self.phrase[0]

	def saveDict(self):
		'''
			Creates a markov chain by looping through each letter in the corpus.
			The results are saved in self.dict
			---
			When a dictionary is being formed:
			> its stored in a histogram in self.dict
			When a dictionary is complete:
			> its put into the self.dict dictionary.
		'''
		self.dict = {}
		for grapheme in self.corpus:
			if grapheme == ' ': # this can be improved greatly
				self.saveWord()
			else:
				self.word += grapheme
		self.saveWord()


if __name__ == '__main__':
	fishy = "One fish two fish, red fish blue fish"
	Model = MarkovChain(fishy, 1)
	print(f"DICTIONARY:\n{Model.dict}\n")
	print(f"UNIQUE TYPES: {Model.types}\n")
	print(f"TOTAL TOKENS: {Model.tokens}\n")