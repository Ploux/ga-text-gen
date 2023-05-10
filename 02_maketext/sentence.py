import random
import datetime

geneSet = "abcdefghijklmnopqrstuvwxyz'"

def makedict(file, newfile=False):
    # this function takes a file and creates a set of all the words
    # newfile is a boolean that determines whether or not to create a new file
    # open the file
    with open(file, 'r') as f:
        # read the file
        text = f.read()
        # split the text into a list of words
        words = text.split()
        # create a set of the words, converting them to lowercase
        wordset = set([word.lower() for word in words])
        # if newfile is true
        if newfile:
            # create a new file
            with open('02_maketext/dict.txt', 'w') as f:
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
        # loop words times
        for i in range(words):
            # initialize the word
            word = ''
            # loop letters times
            for i in range(letters):
                # add a random letter to the word
                word += random.choice(geneSet)
            # add the word to the sentence
            sentence.append(word)
        # append a zero to the sentence for the initial fitness
        sentence.append(0)
        # add the sentence to the list of sentences
        sentences.append(sentence)
    # return the list of sentences
    return sentences

# function to calculate the fitness of sentences
def fitness(sentences, wordset):
    # initialize the fitness
    fitness = 0
    # loop through each sentence
    for sentence in sentences:
        # loop through each word in the sentence
        for word in sentence:
            # if the word is in the wordset
            if word in wordset:
                # add 1 to the fitness
                fitness += 1
    # update the fitness value of the sentence
    sentence[-1] = fitness
    # return the list of sentences
    return sentences

    

# function to display the list of sentences
def display(sentences):
    # capitalize the first letter of the first word
    # put spaces in between the words
    # put a period at the end of the sentence
    # the last word in the sentence is the fitness
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            if i == 0:
                print(sentence[i].capitalize(), end=' ')
            elif i < len(sentence) - 2:
                print(sentence[i], end=' ')
            else:
                print(sentence[i], end='. ')
        print(sentence[-1])

    # print a blank line
    print()
    
test_sentences = sentences(7, 10, 5)
# append a sentence with some real words
test_sentences.append(['hello', 'world', 'this', 'is', 'a', 'test', 'sentence', 'with', 'real', 'words', 0])
display(test_sentences)

wordset = makedict("02_maketext/american-english.txt")

test_sentences = fitness(test_sentences, wordset)
display(test_sentences)

# calculate the fitness of each sentence


# create a wordset and print the first 100 words, the length, and save it to a file
# wordset = makedict("02_maketext/american-english.txt", True)
# print(list(wordset)[:100])
# print(len(wordset))

    