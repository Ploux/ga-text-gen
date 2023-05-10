import random
import datetime

geneSet = "abcdefghijklmnopqrstuvwxyz'"

def makedict(file, newfile=False):
    # this function takes a dictionary and creates a set of all the words
    # newfile is a boolean that determines whether or not to create a new file
    # open the file
    with open(file, 'r') as f:
        # read the file
        text = f.read()
        # split the text into a list of words
        words = text.split()
        # create a set of the words
        wordset = set(words)
        # if newfile is true
        if newfile:
            # create a new file
            with open('dict.txt', 'w') as f:
                # write the wordset to the file
                f.write(str(wordset))
        # return the wordset
        return wordset

# function to generate random sentences
def sentences(num, words, letters):
    # initialize the list of sentences
    sentences = []
    # loop num times
    for i in range(num):
        # initialize the sentence
        sentence = []
        # loop 10 times
        for i in range(words):
            # initialize the word
            word = ''
            # loop 5 times
            for i in range(letters):
                # add a random letter to the word
                word += random.choice(geneSet)
            # add the word to the sentence
            sentence.append(word)
        # add the sentence to the list of sentences
        sentences.append(sentence)
    # return the list of sentences
    return sentences

# function to calculate the fitness of a sentence
# def fitness(sentence, target):

# function to display the list of sentences
def display(sentences):
    # capitalize the first letter of the first word
    # put spaces in between the words
    # put a period at the end of the sentence
    for sentence in sentences:
        print(' '.join(sentence).capitalize() + '.')
    # print a blank line
    print()
    
test_sentences = sentences(5, 10, 5)
display(test_sentences)

# create a wordset and print the first 100 words, the length, and save it to a file
wordset = makedict("02_maketext/american-english.txt", True)
print(list(wordset)[:100])
print(len(wordset))

    