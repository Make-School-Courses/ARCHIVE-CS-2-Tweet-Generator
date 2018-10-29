import random # psuedo-random number generator module
import sys # module allows program to access terminal parameters
import re # the powerful "regular expression" for decompartimentalizing strings

# import palindromes
# import anagrams
# import rearranges
# import histogram

def dictionary_main():
	# opens primary dictionary on the machine.
	'''
		This shouldn't vary too much machine to machine, but it may.
		It is the primary dictionary on your machine, so it holds many words.
		It isn't originally in list format.
	'''
	file = open("/usr/share/dict/words", "r")
	text = file.read()
	file.close()
	return text

def listify_data(input_data):
	# takes data and returns its list version.
	'''
		if its already a list, nothing happens.
		if its a string, it uses REGULAR EXPRESSIONS to transform it into a list.
		if its an unexpected data type, it throws an assertion error
	'''
	if (type(input_data) is str):
		input_data = re.findall(r"[\w']+", input_data)
	assert type(input_data) is list
	return input_data

def randify_list(input_list, max_length):
	# randomly shuffles a list.
	'''
		picks a random digit, min 0 max current length of input list
		pops current digit into output list
	'''
	output_list = []
	while len(input_list) > 0 and len(output_list) < max_length:
		digit_rand = random.randint(0, len(input_list) - 1)
		input_rand = input_list.pop(digit_rand)
		output_list += [input_rand]
		print(output_list)
	print(output_list)
	return output_list

def textify_list(input_list):
	# turns a list into a space-deliminated string.
	'''
		output_text is the final return product.
		each item is added with a space to output_text.
		the final output_text string is returned
	'''
	output_text = ''
	for input_item in input_list:
		if output_text != '':
			output_text += ' '
		output_text += input_item
	input_list = output_text
	return input_list

if __name__ == '__main__':
	data = dictionary_main()
	data = listify_data(data)
	data = randify_list(data,3)
	data = textify_list(data)