def reverse(old_word):
	new_word = ""
	i = 1
	for _ in old_word:
		new_word += old_word[len(old_word)-i]
		i+=1
	return new_word


if __name__ == '__main__':
	print("\nhere's reversed text")
	print("====================")
	print(reverse(input("enter word: >> ")))