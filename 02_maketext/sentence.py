import random
import datetime

geneSet = "abcdefghijklmnopqrstuvwxyz'"

# function to generate random sentences of 10 5 letter words each
def sentences(num):
    # initialize the list of sentences
    sentences = []
    # loop num times
    for i in range(num):
        # initialize the sentence
        sentence = ''
        # loop 10 times
        for i in range(10):
            # initialize the word
            word = ''
            # loop 5 times
            for i in range(5):
                # add a random letter to the word
                word += random.choice(geneSet)
            # add the word to the sentence
            sentence += word + ' '
        # add the sentence to the list of sentences
        sentences.append(sentence)
    # return the list of sentences
    return sentences

print(sentences(5))
