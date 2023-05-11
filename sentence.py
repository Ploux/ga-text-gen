"""
Peter Loux
ECE 8833
Computational Intelligence
Final Project

This program uses a genetic algorithm to generate sentences that are similar to the sentences in a given corpus.

"""


import random
import datetime
import math
from nltk import ngrams
import string

EPOCHS = 10000
NUM_SENTENCES = 10  # number of sentences to generate
NUM_WORDS = 10      # number of words in each initial sentence
NUM_LETTERS = 5     # number of letters in each initial word

MAX_WORDS = 15      # maximum number of words in a sentence
MAX_LETTERS = 15    # maximum number of letters in a word

CROSSOVER_RATE = 0.001  

SENTENCE_MUTATION_RATE = 0.1
SENTENCE_GROWTH_RATE = 0.2      # 0.5 means sentences have equal chance to grow or shrink

WORD_MUTATION_RATE = 0.05
WORD_GROWTH_RATE = 0.9          # 0.5 means words have equal chance to grow or shrink

ADAPT_RATE = 1

geneSet = "abcdefghijklmnopqrstuvwxyz"      

# takes a text file and creates a set of all valid words
def make_word_set(file):
    with open(file, 'r') as f:
        text = f.read()
        words = text.split()
        # set removes duplicates
        wordset = set([word for word in words])
    return wordset

# takes a text file and creates a sorted dictionary of bigrams and their frequencies
def make_bigrams(file):
    filename = 'hound_clean.txt'
    with open(file, 'r') as f:
        text = f.read()
    # split into words by white space
    words = text.split()
    # remove all punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    # convert to lower case
    words = [word.lower() for word in stripped]
    # remove remaining tokens that are not alphabetic
    # for example '“penang' should become 'penang'
    for word in words:
        if not word.isalpha():
            new_word = ''
            for char in word:
                if char.isalpha():
                    new_word += char
            words[words.index(word)] = new_word
    # create bigrams
    bigrams = ngrams(words, 2)
    bigrams_list = list(bigrams)
    # count the frequency of each bigram
    bigram_freq = {}
    for bigram in bigrams_list:
        # don't add any bigrams with the same word twice
        if bigram[0] != bigram[1]:
            if bigram in bigram_freq:
                bigram_freq[bigram] += 1
            else:
                bigram_freq[bigram] = 1
    # sort the bigram frequency dictionary by value
    sorted_bigram_freq = dict(sorted(bigram_freq.items(), key=lambda item: item[1], reverse=True))
    return sorted_bigram_freq

# generates random sentences of gibberish
def generate_sentences(num, words, letters):
    # initialize the list of sentences
    sentences = []
    for i in range(num):
        # initialize the sentence
        sentence = []
        for i in range(words):
            # initialize the word
            word = ''
            for i in range(letters):
                # add a random letter to the word
                word += random.choice(geneSet)
            sentence.append(word)
        # append a zero to the sentence for the initial fitness
        sentence.append(0)
        sentences.append(sentence)
    return sentences

# calculate the fitness of sentences
def fitness(sentences, wordset, corpus):
    for sentence in sentences:
        # initialize the fitness
        fitness = 0
        # loop through each word in the sentence
        for i in range(len(sentence) - 1):
            # if the word is in the wordset, score points
            if sentence[i] in wordset:
                fitness += 0.1*len(sentence[i])
            # if the word is in the corpus, score more points
            if sentence[i] in corpus:
                fitness += len(sentence[i])
        # update the fitness value of the sentence
        sentence[-1] = fitness
        # if two words in a row are the same, make fitness = 0
        for i in range(len(sentence) - 2):
            if sentence[i] == sentence[i + 1]:
                sentence[-1] = 0
    return sentences

# display the list of sentences and their fitness values
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
                print(sentence[i], end='.  ')
        # print the fitness value rounded to 1 decimal place
        print(round(sentence[-1], 1))
    print()
    
# breed the good sentences
def crossover(sentences, corpus, crossover_rate, temp):
    # randomize the order of the sentences
    random.shuffle(sentences)
    # go through each pair of sentences; assume even number of sentences
    for i in range(0, len(sentences), 2):
        # check for crossover
        if random.random() < crossover_rate * temp:
            # pick a random position in the shorter sentence
            pos = random.randint(0, min(len(sentences[i])-2, len(sentences[i + 1])-2))
            # if one sentence has a corpus word at that position and the other doesn't, replace the non-corpus word with the corpus word
            if sentences[i][pos] in corpus and sentences[i + 1][pos] not in corpus:
                sentences[i + 1][pos] = sentences[i][pos]
            elif sentences[i][pos] not in corpus and sentences[i + 1][pos] in corpus:
                sentences[i][pos] = sentences[i + 1][pos]
    # return the sentences
    return sentences

# grow or shrink the sentences
def sentence_mutate(sentences, corpus, sentence_mutate_rate, sentence_growth_rate, max_words, num_letters, temp):
    for sentence in sentences:
        if random.random() < sentence_mutate_rate * temp:
            # determine whether to grow or shrink the sentence
            if random.random() < sentence_growth_rate:
                # if the sentence does not exceed the max number of words
                if len(sentence) < max_words:
                    # add a word at the end (before the fitness value)
                    word = ''
                    for i in range(num_letters):
                        # add a random letter to the word
                        word += random.choice(geneSet)
                    sentence.insert(-1, word)
            else:
                # if the sentence has 3 or more words
                if len(sentence) > 3:
                    # remove a random word if it is not in the corpus
                    word = random.choice(sentence[:-1])
                    if word not in corpus:
                        sentence.remove(word)
    return sentences

# grow or shrink words
def word_mutate(sentences, corpus, wordset, word_mutation_rate, word_growth_rate, temp):
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            # if the word is not in the corpus
            if sentence[i] not in corpus and sentence[i] not in wordset:
                # check for mutation
                if random.random() < word_mutation_rate * temp:
                    # flip a coin, if heads add a letter, if tails remove a letter
                    if len(sentence[i]) < MAX_LETTERS and random.random() < word_growth_rate:
                        # add a letter
                        sentence[i] += random.choice(geneSet)
                    else:
                        if len(sentence[i]) > 1:
                            # remove a letter
                            sentence[i] = sentence[i][:-1]
    return sentences

# adapt the sentences - change random letters to random letters
def adapt(sentences, corpus, wordset, geneSet, adapt_rate):
    # goes through each sentence, if a word is not in the corpus, replace a random letter with a random letter
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            # if the word is not in the corpus
            if sentence[i] not in corpus:
                rand_adapt = random.random()
                # wordset words are much less likely to be adapted
                if (sentence[i] in wordset and rand_adapt < adapt_rate/1000) or (sentence[i] not in wordset and rand_adapt < adapt_rate):
                    # replace a random letter with a random letter (might be the same, this is fine)
                    # choose a random index
                    index = random.randint(0, len(sentence[i]) - 1)
                    # replace the letter at that index with a random letter
                    sentence[i] = sentence[i][:index] + random.choice(geneSet) + sentence[i][index + 1:]
    return sentences

# select the sentences to keep
def selection(sentences, temp):
    # sort the sentences by fitness
    sentences.sort(key=lambda x: x[-1], reverse=True)
    # sum the fitness values
    total_fitness = sum([sentence[-1] for sentence in sentences])
    selected_sentences = []
    for sentence in sentences:
        # calculate the probability of being selected
        prob = (sentence[-1] + 1 / (total_fitness + 1)) * (1/temp)
        # flip a coin, if heads add the sentence to the selected sentences
        if random.random() < prob:
            selected_sentences.append(sentence)
    # figure out how many new sentences to generate
    num_new = len(sentences) - len(selected_sentences)
    # generate new sentences for the bottom
    new_sentences = generate_sentences(num_new, NUM_WORDS, NUM_LETTERS)
    # add the new sentences to the list
    selected_sentences.extend(new_sentences)
    # return the sentences
    return selected_sentences

# remove words that are not in the corpus or the wordset
def format_sentences(sentences, corpus, wordset):
    for sentence in sentences:
        for word in sentence[:-1]:
            # if the word is not in the corpus
            if word not in corpus and word not in wordset:
                # remove it
                sentence.remove(word)
    return sentences

# attempt to put words in bigram order
def bigramify(sentences, corpus, bigrams):
    # loop through the sentences
    for sentence in sentences:
        # loop through the sentence
        for i in range(len(sentence) - 1):
            # if word is in corpus
            if sentence[i] in corpus:
                # look through the bigram dictionary and check all the bigrams starting with that word in order of frequency
                for bigram in bigrams:
                    if bigram[0] == sentence[i]:
                        # search the test sentence for the second word of the bigram
                        # if it is found, swap the next word in the test sentence with the second word of the bigram
                        # and continue looping through the test sentence
                        if bigram[1] in sentence[i+1:]:
                            # swap the words
                            index_to_swap = i + 1 + sentence[i+1:].index(bigram[1])
                            sentence[i+1], sentence[index_to_swap] = sentence[index_to_swap], sentence[i+1]
                            break
    return sentences

# generate initial sentences
sentences = generate_sentences(NUM_SENTENCES, NUM_WORDS, NUM_LETTERS)

# create a wordset
wordset = make_word_set("words_sorted.txt")
corpus = make_word_set("hound_words.txt")
bigrams = make_bigrams("hound_clean.txt")

# calculate the fitness of each sentence
sentences = fitness(sentences, wordset, corpus)

# loop through the epochs
for i in range(EPOCHS):
    temperature = 1 - i/EPOCHS

    # crossover
    sentences = crossover(sentences, corpus, CROSSOVER_RATE, temperature)

    # sentence mutation
    sentences = sentence_mutate(sentences, corpus, SENTENCE_MUTATION_RATE, SENTENCE_GROWTH_RATE, MAX_WORDS, NUM_LETTERS, temperature)
    
    # word mutation
    sentences = word_mutate(sentences, corpus, wordset, WORD_MUTATION_RATE, WORD_GROWTH_RATE, temperature)

    # adaptation
    for j in range(5):
        sentences = adapt(sentences, corpus, wordset, geneSet, ADAPT_RATE)

    # selection
    sentences = selection(sentences, temperature)

    # calculate the fitness of each sentence
    sentences = fitness(sentences, wordset, corpus)

print("Epochs:", i + 1)

# format the sentences by removing words not in the corpus or the wordlist
sentences = format_sentences(sentences, corpus, wordset)
   
mod1_sentences = bigramify(sentences, corpus, bigrams)

display(mod1_sentences)    