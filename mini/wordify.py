import rearrange

def dictionary_main():
	file = open("/usr/share/dict/words", "r")
	text = file.read()
	file.close()
	return text

if __name__ == '__main__':
	text = dictionary_main()
	print(rearrange.rearrange(text, 20))
