import csv


class Node:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.next = None
	def __str__(self):
		return "<Node: (%s, %s), next: %s>" % (self.key, self.value, self.next is not None )
	def __repr__(self):
		return str(self)

# Hash table with separate chaining (kỹ thuật sử lý va chạm)
class HashTable:
	# Initialize hash table
	def __init__(self, capacity):
		self.capacity = capacity #sức chứa
		self.size = 0
		self.buckets = [None]*capacity

	# Input:  key - string
	# Output: Index from 0 to self.capacity
	def hash(self, key):
		hashsum = 0
		# For each character in the key
		for idx, c in enumerate(key): # hàm enumerate thêm vào một bộ đếm vào trước mỗi từ (0,1,2,3...)
			# Add (index + length of key) ^ (current char code)
			hashsum += (idx + len(key)) ** ord(c)
			# Perform modulus to keep hashsum in range [0, self.capacity - 1]
			hashsum = hashsum % self.capacity
		return hashsum

	# Insert a key,value pair to the hashtable
	def insert(self, key, value):
		# 1. Tăng kích thước
		self.size += 1
		# 2. Compute index of key
		index = self.hash(key)
		# Đi đến node tương ứng với hash
		node = self.buckets[index]
		# 3. If bucket is empty:
		if node is None:
			# Create node, add it, return
			self.buckets[index] = Node(key, value)
			return
		# 4. Iterate to the end of the linked list at provided index
		prev = node
		while node is not None:
			prev = node
			node = node.next
		# Add a new node at the end of the list with provided key/value
		prev.next = Node(key, value)

	def find(self, key):
		# 1. Compute hash
		index = self.hash(key)
		# 2. Go to first node in list at bucket
		node = self.buckets[index]
		# 3. Traverse the linked list at this node
		while node is not None and node.key != key:
			node = node.next
		# 4. Now, node is the requested key/value pair or None
		if node is None:
			# Not found
			return None
		else:
			# Found - return the data value
			return node.value

	def remove(self, key):
		# 1. Compute hash
		index = self.hash(key)
		node = self.buckets[index]
		prev = None
		# 2. Iterate to the requested node
		while node is not None and node.key != key:
			prev = node
			node = node.next
		# Now, node is either the requested node or none
		if node is None:
			# 3. Key not found
			return None
		else:
			self.size -= 1
			result = node.value
			if prev is None:
				self.buckets[index] = node.next
			else:
				prev.next = prev.next.next
			return result
def load_csv(filename):
    with open(filename, encoding='utf8') as infile:
        reader = csv.reader(infile.readlines())
    data = []
    for row in reader:
        data.append(row)
    return data

def set_row_csv(filename, data,  word, meaning):
    f = open(filename, "w")
    f.truncate()
    f.close()
    check = True
    for i in range(len(data)):
        if data[i][0] == word:
            data[i][1] = meaning
            check = False
            break
    if check:
        data.append([word, meaning])
    with open(filename, 'a+', encoding='utf8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for row in data:
            writer.writerow(row)

def del_row_csv(filename, data,  word):
    f = open(filename, "w")
    f.truncate() # xóa dữ liệu ở trong file
    f.close()
    for i in range(len(data)):
        if data[i][0] == word:
            data.pop(i)
            break
    with open(filename, 'w', encoding='utf8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for row in data:
            writer.writerow(row)

def get_input(dictionary, data):
    for row in data[1:]:
        dictionary.insert(row[0], row[1])

def process(dictionary, data, filename):
    while True:
        print("====================================")
        print("1. Add a new word")
        print("2. Look-up for word")
        print("3. Remove word")
        print("4. Print size of dictionary")
        print("5. Exit")
        print()
        event = int(input("Choose from 1 to 5: "))
        print()
        if event == 1:
            word = input("Enter word: ").lower()
            meaning = input("Enter word definition: ").lower()
            dictionary.insert(word, meaning)
            set_row_csv(filename, data, word, meaning)
            print(word + ' has been set')
        elif event == 2:
            word = input("Enter word: ").lower()
            if dictionary.find(word) == None:
                print(word, ' is not found in the dictionary')
            else:
                print("Meaning:", dictionary.find(word))
        elif event == 3:
            word = input("Enter word: ").lower()
            dictionary.remove(word)
            print(word + ' has been deleted')
        elif event == 4:
            print("Dictionary size: ", dictionary.size)
        elif event == 5:
            print('Exit')
            break
        else:
            print("Wrong input")
def main():
    print()
    print("======== Load the data file ========")
    filename = input("Enter file name: ")
    try:
        # checking if file is readable and closeable
        handle = open(filename, 'r')  #
        handle.close()
    except IOError:
        print('File is not accessible')
        print("Please enter a valid file!")
    else:
        dictionary = HashTable(1000)
        data = load_csv(filename)
        get_input(dictionary, data)
        process(dictionary, data, filename)
main()