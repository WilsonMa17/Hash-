# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================
# Author: Wilson Ma
# Date: 06/09/2020

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def count(self):
        """counts how many nodes are in a linked list"""
        count = 0
        if self.head is not None:
            cur = self.head
            while cur is not None:
                count += 1
                cur = cur.next
        return count

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self._buckets = []
        for i in range(self.capacity):      # creates empty list and appends empty buckets
            self._buckets.append(LinkedList())
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        index = hash_function_2(key) % self.capacity
        if self._buckets[index].contains(key) is None:
            return None
        return self._buckets[index].contains(key).value # returns the value of the key

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        array = []
        for i in self._buckets:
            if i.head is not None:
                array += [i]
        self.capacity = capacity
        self.clear()
        count = 0
        for i in range(len(self._buckets)):
            for i in array:
                s = i.head
                if i.count() > 1:
                    while s is not None:    # rehashes old keys into new bucket with new hash keys
                        if self._buckets[hash_function_2(s.key) % capacity].contains(s.key) is None:
                            self._buckets[hash_function_2(s.key) % capacity].add_front(s.key, s.value)
                            self.size = self.size + 1
                        s = s.next
                        count += 1
                else:
                    x = (i.head.key)
                    a = i.head.value
                    if self._buckets[hash_function_2(x) % capacity].contains(x) is None:
                        self._buckets[hash_function_2(x) % capacity].add_front(x , a)
                        self.size = self.size + 1

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        index = hash_function_2(key) % self.capacity
        if self._buckets[index].contains(key) is None:   # if key does not exists, creates new node
            self._buckets[index].add_front(key, value)
            self.size = self.size + 1
        else:
            self._buckets[index].contains(key).value = value    # updates value if key already exists

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        index = hash_function_2(key) % self.capacity

        if self._buckets[index].contains(key):
            if self._buckets[index].head.key == key:   # if first link equals key,removes
                self._buckets[index].head = self._buckets[index].head.next
            else:
                cur = self._buckets[index].head
                while cur:      # iterate through linked list to find val to be removed
                    prev = cur
                    cur = cur.next
                    s = cur
                    if cur.key == key:
                        break
                prev.next = s.next
        else:
            return

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """

        index = hash_function_2(key) % self.capacity
        if self._buckets[index].contains(key) is None:
            return False
        else:
            return True

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        count = 0
        index = 0
        for i in range(self.capacity):
            if self._buckets[index].head is None:
                count += 1
            index += 1
        return count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        l=0
        t=0
        len(self._buckets)
        for i in range(self.capacity):      # counts total number of linked list in bucket
            t += self._buckets[l].count()
            l += 1
        return float(t / len(self._buckets))

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out