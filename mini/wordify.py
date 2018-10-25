import rearrange

def wordify():
	file = open("/usr/share/dict/words","r")
	text = file.read()
	file.close()

if __name__ == '__main__':
	print(rearrange.rearrange(text, 20))