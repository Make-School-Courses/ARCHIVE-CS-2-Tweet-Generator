from flask import Flask
app = Flask(__name__)

import urllib.request # imports internet textfile reader
import random # psuedo-random number generator module
import sys # module allows program to access terminal parameters
import re # the powerful "regular expression" for decompartimentalizing strings

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

def publication_random():
	book = round((random.random()*49544)+1)
	link = f"http://www.gutenberg.org/cache/epub/{book}/pg{book}.txt"
	with urllib.request.urlopen(link) as response:
		text = response.read()
	print("200 SUCCESS")
	text = str(text)
	text = text.replace("\\r\\n", "")
	return text

def publication_example():
	# opens primary dictionary on the machine.
	'''
		It is the primary dictionary on your machine, so it holds many words.
		It isn't originally in list format.
	'''
	file = open("./example.txt", "r")
	text = file.read()
	file.close()
	return text

def user_number(feed):
	print(feed)
	while True:
		try:
			number = int(input("enter integer:\n>> "))
			assert isinstance(number, int) # throws an error if its not an integer
			assert number != None
			assert number != ""
			return number
		except:
			print("INVALID INPUT.\nplease try again.\n")

def user_string(feed):
	print(feed)
	while True:
		try:
			string = str(input("enter string:\n>> "))
			assert isinstance(string, str) # throws an error if its not an string
			return string
		except:
			print("INVALID INPUT.\nplease try again.\n")

def listify_data(input_data):
	# takes data and returns its list version.
	'''
		if its already a list, nothing happens.
		if its a string, it uses REGULAR EXPRESSIONS to transform it into a list.
		if its an unexpected data type, it throws an assertion error
	'''
	input_data = str(input_data)
	if (type(input_data) is str):
		input_data = re.findall(r"[\w']+", input_data)
		# I still must configure the thing to remove /n /r /xc3
	assert type(input_data) is list
	return input_data

def undupli_list(input_list):
	# removes duplicates from a list.
	output_list = []
	for word in input_list:
		if word not in output_list:
			output_list += [word]
	return output_list

def randify_list(input_list, iterations):
	# randomly shuffles a list.
	'''
		picks a random digit, min 0 max current length of input list
		pops current digit into output list
		the `iterations` variable determines the number of words to output
	'''
	output_list = []
	while len(input_list) > 0 and (len(output_list) < iterations or iterations == 0):
		digit_rand = random.randint(0, len(input_list) - 1)
		input_rand = input_list.pop(digit_rand)
		output_list += [input_rand]
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

def textify_dict(input_dict):
	output_text = ''
	for w in sorted(input_dict, key=input_dict.get, reverse=False):
		if input_dict[w] > 0:
			output_text += str(input_dict[w]) + ' ' + str(w) + "\n"
	return output_text

def lowerfy_list(input_list):
	# takes a list of strings and runs lowercase on each item.
	'''
		output_text is the final return product.
		each item is added with a space to output_text.
		the final output_text string is returned
	'''
	output_list = []
	for string in input_list:
		string = string.lower()
		output_list += [string]
	return output_list

def reverse_text(old_word):
	# simply reverses a text.
	new_word = ""
	i = 1
	for _ in old_word:
		new_word += old_word[len(old_word)-i]
		i+=1
	return new_word


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
	Now setting up specific functions. These will each return complete jobs.
	These functions will use the previously declared helpers to make code readable.
'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def rearrange(iterations, input_data = dictionary_main()):
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	# data = undupli_list(data) ## This function takes too long!
	data = randify_list(data, iterations)
	data = textify_list(data)
	return(data)

### ANAGRAMS

def anagrams (input_word, input_data = dictionary_main()):
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	new_data = []
	i_word = input_word
	for v_word in data:
		if verify_anagram(i_word,v_word):
			new_data += [v_word]
	new_data = textify_list(new_data)
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

### PALINDROMES

def palindromes(input_data = dictionary_main()):
	data = input_data
	data = listify_data(data)
	data = lowerfy_list(data)
	new_data = []
	for word in data:
		if verify_palindrome(word):
			new_data += [word]
	new_data = undupli_list(new_data)
	new_data = textify_list(new_data)
	return new_data

def verify_palindrome(input_word):
	i = 1
	while (i <= len(input_word)/2):
		if input_word[i-1] != input_word[-i]:
			return False
		i += 1
	return True

# HISTOGRAM

def histogram(input_data = dictionary_main()):
	data = listify_data(input_data)
	data = lowerfy_list(data)
	# data = undupli_list(data) ## This removes duplicates. If this is correct, there will be no outputs when this is uncommented.
	hist = {}
	for word in data:
		if word in hist:
			hist[word] += 1
		else:
			hist[word] = 1
	return hist

def histogram_arrays(input_data = dictionary_main()):
	data = listify_data(input_data)
	data = lowerfy_list(data)
	hist = []

	for word in data:
		found = False
		for item in hist:
			if word == item[0]:
				found = True
		if found:
			item[1] += 1
		else:
			item[0] = word
			item[1] = 1
	return hist

def display_dict(input_data = dictionary_main()):
	hist = histogram(input_data)
	output = textify_dict(hist)
	return output

def display_weight(input_data):
	hist = histogram(input_data)
	hist = calculate_weight(hist) # testing calculate weight
	string = prettify(hist)
	return string

def prettify(input_data):
	string = ''
	for item in input_data:
		string += item
		string += ': '
		string += str(input_data[item] * 1000)
		string += '‰\n'
	return string


# WEIGHTED FUNCTION

def calculate_weight(input_dict):
	weight_dict = {}
	dict_total = 0
	for word in input_dict:
		dict_total += input_dict[word]
	for word in input_dict:
		weight_dict[word] = input_dict[word] / dict_total
	return weight_dict

def random_choice(weight_dict):
	cumulative = 0
	rand_select = random.random()
	for word in weight_dict:
		if (cumulative <= rand_select < weight_dict[word] + cumulative):
			print("SELECTED: " + word)
			return word
		cumulative += weight_dict[word]
	print(rand_select)
	# for word in weight_dict:
	# 	if weight_dict


### STARTER KIT
# MUST DO RANDOM WEIGHTING

@app.route('/')
def hello_world():
	return display_weight(publication_random())

if __name__ == '__main__':
	# print("\nIt looks like you used a parameter when you ran this file.\nI'm going to assume that this is a file, and I'm going to run")

	entry = user_number("\nI generate several words.\nHow many should I create?")
	print("\nRandom Words:\n" + rearrange(entry))

	entry = user_string("\nI make anagrams, so I need a word.\nWhat base word should I use today?")
	print("\nAnagrams:\n" + anagrams(entry))

	print("\nI do palindromes too, but I\ndon't need any inputs for that!\nI'll go ahead and get started.")
	print("\nPalindromes:\n" + palindromes())

	print("\nI'm going to spit out a large histogram of words, \nsorted by the PERMILLE (‰) of the text that it is used in.")
	input("press enter to continue: ")
	my_dict = publication_random()
	print("\nDisplay Weight:\n" + display_weight(my_dict))