'''
extract text from corpus
clean text

create word-pair
create dictionary

for each character in corpus:
	if next character is ' '
		clear word-pair
		next character
	else:
		add character to word
		next character
'''

def clean(corpus):
	return corpus

def makeDict(corpus):
	string = ''
	for grapheme in corpus:
		if grapheme == ' ':
			pass
			# skip
			# save to word
		else:
			pass
