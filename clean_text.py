"""
Peter Loux Sr
ECE 8833 - Computational Intelligence
Final Project
May 11, 2023

This program is used to generate a list of words from the text of the book which is used as the corpus.
"""

# load text
filename = 'hound_clean.txt'
file = open(filename, 'rt' )
text = file.read()
file.close()

# split into words by white space
words = text.split()
print(words[:100])
print()

# remove all punctuation
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in words]
print("Removed punctuation:")
print(stripped[:100])
print()

# convert to lower case
words = [word.lower() for word in stripped]
print("Lower case:")
print(words[:100])
print()

# remove remaining tokens that are not alphabetic
# for example '“penang' should become 'penang'
for word in words:
    if not word.isalpha():
        new_word = ''
        for char in word:
            if char.isalpha():
                new_word += char
        words[words.index(word)] = new_word
print("Removed non-alphabetic:")
   
print(words[:100])

# convert to set to remove duplicates
words = set(words)
# print(words)

# sort words by length
words = sorted(words, key=len)

# save to file, one word per line
filename = 'hound_words.txt'
data = '\n'.join(words)
file = open(filename, 'w')
file.write(data)
file.close()
