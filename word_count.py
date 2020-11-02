# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        sorted1 = {}
        array = []
        count = 0
        for line in f:
            words = rgx.findall(line)
            for w in words:
                array += [w.lower()]
                index = hash_function_2(w.lower()) % ht.capacity
                if ht._buckets[index].contains(w.lower()) is None:      # adds words in hash bucket
                    ht._buckets[index].add_front(w.lower(), array.count(array[count]))
                    sorted1[w.lower()] = array.count(array[count])
                else:
                    ht._buckets[index].contains(w.lower()).value = array.count(array[count])
                    sorted1[w.lower()] = array.count(array[count])
                count += 1
    sort_orders = sorted(sorted1.items(), key= lambda x: x[1],reverse = True)
    s= 0
    i = 0
    array = []
    while s < number:   # gets predefined number of top words
        s += 1
        array += [(sort_orders[i])]
        i += 1
    return array

#print(top_words("alice.txt",5))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE