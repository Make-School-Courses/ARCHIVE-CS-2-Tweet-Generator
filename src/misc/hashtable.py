#!python

from .linkedlist import LinkedList


class HashTable:
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
		items = [f"{key!r}: {val!r}" for key, val in self.items()]
		return "{" + ", ".join(items) + "}"

	def __repr__(self):
		"""
		Return a string representation of this hash table.
		"""
		return f"HashTable({self.items()!r})"

	def _bucket_index(self, key):
		"""
		Return the bucket index where the given key would be stored.
		"""
		# Calculate the given key's hash code and transform into bucket index
		return hash(key) % len(self.buckets)

	def keys(self):
		"""
		Return a list of all keys in this hash table.

		Running time: O(b*x = n) | b = buckets & x = avg size of buckets, n/b
		With a nested for loop, we must run the 2nd loop for each item in the 1st loop.
		"""
		# Collect all keys in each bucket
		all_keys = []
		for bucket in self.buckets:
			# Collect all values in each bucket
			for key, _ in bucket.items():
				all_keys.append(key)
		return all_keys

	def values(self):
		"""
		Return a list of all values in this hash table.

		Running time: O(b*x = n) | b = buckets & x = avg size of buckets, n/b
		With a nested for loop, we must run the 2nd loop for each item in the 1st loop.
		"""
		all_values = []
		# Loop through all buckets
		for bucket in self.buckets:
			# Collect all values in each bucket
			for _, value in bucket.items():
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

	def contains(self, my_key):
		"""
		Return True if this hash table contains `my_key`, or False.

		Running time: O(l = n÷b) | b = buckets & n = total num of entries
		The number of items we have is evenly divided among each bucket.
		This means that we just have to traverse one bucket's worth of data, or l.
		"""
		# Find bucket where `my_key` belongs
		index = self._bucket_index(my_key)
		bucket = self.buckets[index]
		# Check if key-value entry exists in bucket
		return any(key == my_key for key, _ in bucket.items())

	def get(self, my_key):
		"""
		Return the value associated with `my_key`, or raise KeyError.

		Running time: O(l = n÷b) | b = buckets & n = total num of entries
		The number of items we have is evenly divided among each bucket.
		This means that we just have to traverse one bucket's worth of data, or l.
		"""
		# Find bucket where `my_key` belongs
		index = self._bucket_index(my_key)
		bucket = self.buckets[index]
		# Check if key-value entry exists in bucket
		for key, value in bucket.items():
			# If found, return the value associated with `my_key`
			if key == my_key:
				return value
		# Otherwise, raise error to tell user get failed
		raise KeyError(f"Key not found: {my_key}")

	def set(self, my_key, my_value):
		"""
		Insert or update `my_key` and its associated value.

		Running time: O(l = n÷b) | b = buckets & n = total num of entries
		It has to run contains(), which has the highest Order in this function
		"""
		# Find bucket where `my_key` belongs
		index = self._bucket_index(my_key)
		bucket = self.buckets[index]
		# Delete key-value entry if it exists in bucket
		if self.contains(my_key):
			self.delete(my_key)
		# Create a new key-value pair
		bucket.prepend((my_key, my_value))

	def delete(self, my_key):
		"""
		Delete `my_key` from this hash table, or raise KeyError.

		Running time: O(l = n÷b) | b = buckets & n = total num of entries
		This function inherits the linked list's delete function, Order of O(n).
		However, this is reduced to l because of how the buckets split up each linked list.
		"""
		# Find bucket where `my_key` belongs
		index = self._bucket_index(my_key)
		bucket = self.buckets[index]

		# Create quality to pass into find()
		def quality(data):
			return data[0] == my_key

		result = bucket.find(quality)
		# Check if key-value entry exists in bucket, and delete it
		if result:
			bucket.delete(result)
		# Otherwise, raise error to tell user delete failed
		else:
			raise KeyError(f"Key not found: {my_key}")


def test_hash_table():
	ht = HashTable()
	print(f"hash table: {ht}")

	print("\nTesting set:")
	for key, value in [("I", 1), ("V", 5), ("X", 10)]:
		print(f"set({key!r}, {value!r})")
		ht.set(key, value)
		print(f"hash table: {ht}")

	print("\nTesting get:")
	for key in ["I", "V", "X"]:
		value = ht.get(key)
		print(f"get({key!r}): {value!r}")

	print("contains({!r}): {}".format("X", ht.contains("X")))
	print(f"length: {ht.length()}")

	# Enable this after implementing delete method
	delete_implemented = False
	if delete_implemented:
		print("\nTesting delete:")
		for key in ["I", "V", "X"]:
			print(f"delete({key!r})")
			ht.delete(key)
			print(f"hash table: {ht}")

		print("contains(X): {}".format(ht.contains("X")))
		print(f"length: {ht.length()}")


if __name__ == "__main__":
	test_hash_table()
