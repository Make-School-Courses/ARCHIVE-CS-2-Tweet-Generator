import rearrange
f = open("/usr/share/dict/words","r")


if __name__ == '__main__':
	print(rearrange.rearrange(f.read()), 20)