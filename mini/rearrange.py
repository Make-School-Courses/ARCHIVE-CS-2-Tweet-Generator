import random # psuedo-random number generator module
import sys # module allows program to access terminal parameters
import re # the powerful "regular expression" for decompartimentalizing strings

def rearrange(input_data, max_length=20):
	data = input_data
	data = listify_data(data) # creates a list from text
	data = randify_list(data, max_length) # randomizes list sequence
	data = textify_list(data) # morphes a list into text
	return data

def listify_data(input_data):
	if (type(input_data) is str):
		input_data = re.findall(r"[\w']+", input_data)
	assert type(input_data) is list
	return input_data

def randify_list(input_list, max_length):
	output_list = []
	while len(input_list) > 0 and len(output_list) < max_length:
		digit_rand = random.randint(0, len(input_list) - 1)
		input_rand = input_list.pop(digit_rand)
		output_list += [input_rand]
	return output_list

def textify_list(input_list):
	output_text = ''
	for input_item in input_list:
		if output_text != '':
			output_text += ' '
		output_text += input_item
	return output_text

if __name__ == '__main__':
	input_list = sys.argv[1:]
	print(rearrange(input_list))