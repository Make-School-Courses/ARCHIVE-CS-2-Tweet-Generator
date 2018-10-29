import rearrange

def anagramify_data(input_data, input_word): # anagrange = anagram arrange
	data = input_data
	data = rearrange.listify_data(data)
	i_word = input_word
	new_data = []
	for v_word in data:
		# print(f"\nanagram: {i_word}\nversus: {v_word}")
		if verify_anagram(i_word,v_word):
			new_data += [v_word]
	new_data = rearrange.textify_list(new_data)
	return new_data

def verify_anagram(input_word, verify_word):
	input_list = list(input_word)
	verify_list = list(verify_word)
	input_list.sort()
	verify_list.sort()
	if input_list == verify_list:
		return True
	else:
		return False