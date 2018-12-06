#!python

class Node(object):

	def __init__(self, data):
		"""
			Initialize this node with the given data.
		"""
		self.data = data
		self.next = None

	def __repr__(self):
		"""
			Return a string representation of this node.
		"""
		return 'Node({!r})'.format(self.data)

class LinkedList(object):

	def __init__(self, items=None):
		"""
			Initialize this linked list and append the given items, if any.
		"""
		self.size = 0 # Keeps track of node size
		self.head = None  # First node
		self.tail = None  # Last node
		# Append given items
		if items is not None:
			for item in items:
				self.append(item)

	def __str__(self):
		"""
			Return a formatted string representation of this linked list.
		"""
		items = ['({!r})'.format(item) for item in self.items()]
		return '[{}]'.format(' -> '.join(items))

	def __repr__(self):
		"""
			Return a string representation of this linked list.
		"""
		return 'LinkedList({!r})'.format(self.items())

	def items(self):
		"""
			Return a list (dynamic array) of all items in this linked list.

			Best and worst case running time: O(n) for n items in the list (length)
			because we always need to loop through all n nodes to get each item.
		"""
		items = []  # O(1) time to create empty list
		# Start at head node
		node = self.head  # O(1) time to assign new variable
		# Loop until node is None, which is one node too far past tail
		while node is not None:  # Always n iterations because no early return
			items.append(node.data)  # O(1) time (on average) to append to list
			# Skip to next node to advance forward in linked list
			node = node.next  # O(1) time to reassign variable
		# Now list contains items from all nodes
		return items  # O(1) time to return list

	def is_empty(self):
		"""
			Return a boolean indicating whether this linked list is empty.

			Running time: O(1)
			There are no loops; it just has to compute each action once
		"""
		return self.head is None

	def length(self):
		"""
			Return the length of this linked list by traversing its nodes.

			Running time: O(1)
			I used a parameter, so all I need to do is access it.
		"""
		# Access and return node size parameter.
		# Couldn't call it length because its used here!
		return self.size

	def append(self, data):
		"""
			Insert the given data at the tail of this linked list.

			Running time: O(1)
			There are no loops; it just has to compute each action once
		"""
		# Add one to node size
		self.size += 1
		# Create new node to hold given data
		new_node = Node(data)
		# Append node after tail if it exists
		if self.head != None:
			self.tail.next = new_node
		# Set first node if it doesn't exist
		else:
			self.head = new_node
		# Set tail to the last node -- new_node
		self.tail = new_node

	def prepend(self, data):
		"""
			Insert the given data at the head of this linked list.

			Running time: O(1)
			There are no loops; it just has to compute each action once
		"""
		# Add one to length
		self.size += 1
		# Create new node to hold given data
		new_node = Node(data)
		# Prepend node before head node, if it exists
		if self.head != None:
			new_node.next = self.head
		# if it doesn't exist, than this node is the first and last
		else:
			self.tail = new_node
		# Set head to the first node -- new_node
		self.head = new_node

	def find(self, quality):
		"""
			Return data from this linked list satisfying the given quality.

			Best case running time: O(1)
			If the find function immediately finds the first node as valid...
			...then it only uses the while loop once.
			---
			Worst case running time: O(n)
			If the find function never finds valid data...
			...then it has to loop through all (n) nodes in the linked list.
		"""
		# Loop through all nodes to find one node's data where quality(data) is True
		get_node = self.head
		while get_node != None:
			# Check if this node's data satisfies given quality function.
			if quality(get_node.data) == True:
				return get_node.data
			# If it doesn't, search the next node, if there is one.
			else:
				get_node = get_node.next
		# Otherwise, nothing has been found.
		else:
			return None


	def delete(self, data):
		"""
			Delete the given item from this linked list, or raise ValueError.

			Best case running time: O(1)
			If the loop is exited on the first try (eg. head is result)...
			...then it only has each computation in the loop once
			---
			Worst case running time: O(n)
			If the loop is totally complete
		"""
		print('\nSTARTING DELETE FUNCTION')
		print(f"here's the input data: {data}\n")

		# prv_node and get_node keeps track of two consecutive nodes.
		prv_node = None
		get_node = self.head
		found = False

		# LOOP THROUGH ALL NODES TO FIND ONE NODE'S DATA THAT MATCHES INPUT
		while get_node != None:
			# If this node's data equals the input, skip around it.
			if get_node.data == data:
				found = True
				# Set Head & Tail
				if (prv_node == None) and (get_node.next == None):
					self.head = None
					self.tail = None
				# Set Head
				elif prv_node == None:
					self.head = get_node.next
					get_node = None
				# Set Tail
				elif get_node.next == None:
					self.tail = prv_node
					get_node = None
					prv_node.next = None
				# Set Node
				else:
					prv_node.next = get_node.next
				break
			# otherwise, check the next node.
			else:
				prv_node = get_node
				get_node = get_node.next

		if found:
			print('entry found! reducing size.\n')
			self.size -= 1
		else:
			raise ValueError(f'Item not found: {data}')

def test_linked_list():
	ll = LinkedList()
	print('list: {}'.format(ll))

	print('\nTesting append:')
	for item in ['A', 'B', 'C']:
		print('append({!r})'.format(item))
		ll.append(item)
		print('list: {}'.format(ll))

	print('head: {}'.format(ll.head))
	print('tail: {}'.format(ll.tail))
	print('length: {}'.format(ll.length()))

	# Enable this after implementing delete method
	delete_implemented = False
	if delete_implemented:
		print('\nTesting delete:')
		for item in ['B', 'C', 'A']:
			print('delete({!r})'.format(item))
			ll.delete(item)
			print('list: {}'.format(ll))

		print('head: {}'.format(ll.head))
		print('tail: {}'.format(ll.tail))
		print('length: {}'.format(ll.length()))

if __name__ == '__main__':
	test_linked_list()