#!python

from linkedlist import LinkedList

class HashTable(object):
	def __init__(self, init_size=8):
		"""
			Initialize this hash table with the given initial size.
		"""
		# Create a new list (used as fixed-size array) of empty linked lists
		self.buckets = [LinkedList() for _ in range(init_size)]

	def __str__(self):
		"""
			Return a formatted string representation of this hash table.
		"""
		items = ['{!r}: {!r}'.format(key, val) for key, val in self.items()]
		return '{' + ', '.join(items) + '}'

	def __repr__(self):
		"""
			Return a string representation of this hash table.
		"""
		return 'HashTable({!r})'.format(self.items())

	def _bucket_index(self, key):
		"""
			Return the bucket index where the given key would be stored.
		"""
		# Calculate the given key's hash code and transform into bucket index
		return hash(key) % len(self.buckets)

	def keys(self):
		"""
			Return a list of all keys in this hash table.

			Running time: O(b×l = n) | b = buckets & l = avg size of buckets, n÷b
			With a nested for loop, we must run the 2nd loop for each item in the 1st loop.
		"""
		# Collect all keys in each bucket
		all_keys = []
		for bucket in self.buckets:
			# Collect all values in each bucket
			for key, value in bucket.items():
				all_keys.append(key)
		return all_keys

	def values(self):
		"""
			Return a list of all values in this hash table.

			Running time: O(b×l = n) | b = buckets & l = avg size of buckets, n÷b
			With a nested for loop, we must run the 2nd loop for each item in the 1st loop.
		"""
		all_values = []
		# Loop through all buckets
		for bucket in self.buckets:
			# Collect all values in each bucket
			for key, value in bucket.items():
				all_values.append(value)
		return all_values

	def items(self):
		"""
			Return a list of all items (key-value pairs) in this hash table.

			Running time: O(b) | b = buckets & l = avg size of buckets, n÷b
			There is only one for loop -- that's for each bucket.
			The extend function is O(1) so its not influencing the final Order.
		"""
		# Collect all pairs of key-value entries in each bucket
		all_items = []
		for bucket in self.buckets:
			all_items.extend(bucket.items())
		return all_items

	def length(self):
		"""
			Return the number of key-value entries by traversing its buckets.

			Running time: O(b) | b = buckets & l = avg size of buckets, n÷b
			Because size is a parameter in LinkedList, the program loops through each bucket and adds that to counter.
		"""
		counter = 0
		# Loop through all buckets
		for bucket in self.buckets:
			# Count number of key-value entries in each bucket
			counter += bucket.size
		return counter

	def contains(self, myKey):
		"""
			Return True if this hash table contains myKey, or False.

			Running time: O(l = n÷b) | b = buckets & n = total num of entries
			The number of items we have is evenly divided among each bucket.
			This means that we just have to traverse one bucket's worth of data, or l.
		"""
		# Find bucket where myKey belongs
		index = self._bucket_index(myKey)
		bucket = self.buckets[index]
		# Check if key-value entry exists in bucket
		for key, value in bucket.items():
			if key == myKey:
				return True
		# Otherwise, return False
		else:
			return False

	def get(self, myKey):
		"""
			Return the value associated with the myKey, or raise KeyError.

			Running time: O(l = n÷b) | b = buckets & n = total num of entries
			The number of items we have is evenly divided among each bucket.
			This means that we just have to traverse one bucket's worth of data, or l.
		"""
		# Check if key-value entry exists in bucket
		if contains(myKey):
			# If found, find bucket where myKey belongs
			index = self._bucket_index(myKey)
			bucket = self.buckets[index]
			# If found, return value associated with myKey
			for key, value in bucket.items():
				if key == myKey:
					return value
		# Otherwise, raise error to tell user get failed
		else:
			raise KeyError(f'Key not found: {key}')

	def set(self, key, value):
		"""
			TODO: Insert or update the given key with its associated value.

			TODO: Running time: O(???)
			TODO: Why and under what conditions?
		"""
		# Check if key-value entry exists in bucket
		if contains(key):
			# If found, find bucket where given key belongs
			index = self._bucket_index(key)
			# TODO: If found, update value associated with given key
		else:
			# TODO: Otherwise, insert given key-value entry into bucket

	def delete(self, key):
		"""
			TODO: Delete the given key from this hash table, or raise KeyError.

			TODO: Running time: O(???)
			TODO: Why and under what conditions?
		"""
		# Find bucket where given key belongs
		index = self._bucket_index(key)
		# TODO: Check if key-value entry exists in bucket
		# TODO: If found, delete entry associated with given key
		# TODO: Otherwise, raise error to tell user delete failed
		# Hint: raise KeyError('Key not found: {}'.format(key))


def test_hash_table():
	ht = HashTable()
	print('hash table: {}'.format(ht))

	print('\nTesting set:')
	for key, value in [('I', 1), ('V', 5), ('X', 10)]:
		print('set({!r}, {!r})'.format(key, value))
		ht.set(key, value)
		print('hash table: {}'.format(ht))

	print('\nTesting get:')
	for key in ['I', 'V', 'X']:
		value = ht.get(key)
		print('get({!r}): {!r}'.format(key, value))

	print('contains({!r}): {}'.format('X', ht.contains('X')))
	print('length: {}'.format(ht.length()))

	# Enable this after implementing delete method
	delete_implemented = False
	if delete_implemented:
		print('\nTesting delete:')
		for key in ['I', 'V', 'X']:
			print('delete({!r})'.format(key))
			ht.delete(key)
			print('hash table: {}'.format(ht))

		print('contains(X): {}'.format(ht.contains('X')))
		print('length: {}'.format(ht.length()))

if __name__ == '__main__':
	test_hash_table()