import random
import datetime

geneSet = "abcdefghijklmnopqrstuvwxyz'"

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
def fitness(sentence, target):

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

    