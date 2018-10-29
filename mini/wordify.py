import rearrange

def dictionary_main():
	file = open("/usr/share/dict/words", "r")
	text = file.read()
	file.close()
	return text

if __name__ == '__main__':
	text = dictionary_main()
	print("\nhere's rearranged text")
	print("======================")
	print(rearrange.rearrange(text, 20))

	print("\nhere's palindrome text")
	print("======================")
	print(rearrange.palindrome(text))

	print("\nhere's anagramify text")
	print("======================")
	print(rearrange.anagrange(text,input("enter word: >> ")))
