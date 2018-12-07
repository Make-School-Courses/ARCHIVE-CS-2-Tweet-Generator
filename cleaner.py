def getCorpus(file):
	with open(f'{file}', 'r') as myfile:
		data = myfile.read()
	return data

def clean(corpus, filter):
	cleaned = ''
	for grapheme in corpus:
		for checker in filter:
			if grapheme == checker:
				cleaned += grapheme
				break
			elif grapheme == "\n":
				cleaned += ' '
			else:
				pass
	return cleaned


if __name__ == '__main__':
	corpus = getCorpus('dnd_phb.txt')
	filter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 .,;!?"
	cleaned = clean(corpus, filter)
	print(cleaned)