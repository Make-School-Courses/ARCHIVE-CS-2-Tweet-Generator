def palindromify_data(input_data):
	data = input_data
	data = listify_data(data)
	new_data = []
	for word in data:
		if verify_palindrome(word):
			new_data += [word]
	new_data = textify_list(new_data)
	return new_data

def verify_palindrome(input_word):
	i = 1
	while (i <= len(input_word)/2):
		if input_word[i-1] != input_word[-i]:
			return False
		i += 1
	return True
