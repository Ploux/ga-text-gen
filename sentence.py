import random
import datetime


EPOCHS = 10000
NUM_SENTENCES = 20
NUM_WORDS = 10
NUM_LETTERS = 5
MAX_WORDS = 20

CROSSOVER_RATE = 0.01

SENTENCE_MUTATION_RATE = 0.1
SENTENCE_GROWTH_RATE = 0.5 # 0.5 means sentences have equal chance to grow or shrink


WORD_MUTATION_RATE = 1
WORD_GROWTH_RATE = 0.8 # 0.5 means words have equal chance to grow or shrink
ADAPT_RATE = 1
SELECT_RATE = 0.5

geneSet = "abcdefghijklmnopqrstuvwxyz"

def make_word_set(file):
    # this function takes a file and creates a set of all the words
    # open the file
    with open(file, 'r') as f:
        # read the file
        text = f.read()
        # split the text into a list of words
        words = text.split()
        wordset = set([word for word in words])
        # return the wordset
    return wordset

def make_corpus(file):
    # this function takes a file and creates a set of all the words
    # open the file
    with open(file, 'r') as f:
        # read the file
        text = f.read()
        # split the text into a list of words
        words = text.split()
        corpus = set([word for word in words])
        # return the wordset
    return corpus

# function to generate random sentences
def generate_sentences(num, words, letters):
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
def fitness(sentences, wordset, corpus):
    # initialize the fitness
    # loop through each sentence
    for sentence in sentences:
        fitness = 0
        # loop through each word in the sentence
        for i in range(len(sentence) - 1):
            # if the word is in the wordset
            if sentence[i] in wordset:
                fitness += 0.1*len(sentence[i])
            # if the word is in the corpus
            if sentence[i] in corpus:
                fitness += len(sentence[i])
        # update the fitness value of the sentence
        sentence[-1] = fitness
        # if two words in a row are the same, make fitness = 0
        for i in range(len(sentence) - 2):
            if sentence[i] == sentence[i + 1]:
                sentence[-1] = 0
                
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
                print(sentence[i], end='.  ')
        # print the fitness value rounded to 1 decimal place
        print(round(sentence[-1], 1))
    print()
    
# function to breed the sentences
def crossover(sentences, corpus, crossover_rate):
    # randomize the order of the sentences
    random.shuffle(sentences)
    # go through each pair of sentences; for now assume even number of sentences
    for i in range(0, len(sentences), 2):
        # check for crossover
        if random.random() < crossover_rate:
            # pick a random position in the shorter sentence
            pos = random.randint(0, min(len(sentences[i])-2, len(sentences[i + 1])-2))
            # if one sentence has a corpus word at that position and the other doesn't replace the non-corpus word with the corpus word
            if sentences[i][pos] in corpus and sentences[i + 1][pos] not in corpus:
                sentences[i + 1][pos] = sentences[i][pos]
            elif sentences[i][pos] not in corpus and sentences[i + 1][pos] in corpus:
                sentences[i][pos] = sentences[i + 1][pos]
    # return the sentences
    return sentences

def sentence_mutate(sentences, corpus, sentence_mutate_rate, sentence_growth_rate, max_words, num_letters):
    for sentence in sentences:
        if random.random() < sentence_mutate_rate:
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
                if len(sentence) >= 3:
                    # remove a random word if it is not in the corpus
                    word = random.choice(sentence[:-1])
                    if word not in corpus:
                        sentence.remove(word)
    return sentences

def word_mutate(sentences, wordset, WORD_MUTATION_RATE):
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            # if the word is not in the wordset
            if sentence[i] not in wordset:
                # flip a coin, if heads add a letter, if tails remove a letter
                if random.random() < WORD_MUTATION_RATE:
                    # flip a coin, if heads add a letter, if tails remove a letter
                    if len(sentence[i]) < 15 and random.random() < WORD_GROWTH_RATE:
                        # add a letter
                        sentence[i] += random.choice(geneSet)
                    else:
                        if len(sentence[i]) > 1:
                            # remove a letter
                            sentence[i] = sentence[i][:-1]
    return sentences

def adapt(sentences, wordset, ADAPT_RATE):
    # goes through each sentence, if a word is not in the wordset, replace a random letter with a random letter
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            # if the word is not in the wordset
            if sentence[i] not in wordset:
                if random.random() < ADAPT_RATE:
                    # replace a random letter with a random letter (might be the same, this is fine)
                    # choose a random index
                    index = random.randint(0, len(sentence[i]) - 1)
                    # replace the letter at that index with a random letter
                    sentence[i] = sentence[i][:index] + random.choice(geneSet) + sentence[i][index + 1:]
                    # sentence[i] = sentence[i][:random.randint(0, len(sentence[i]) - 1)] + random.choice(geneSet) + sentence[i][random.randint(0, len(sentence[i]) - 1):]
    return sentences

def selection(sentences):
    # sort the sentences by fitness
    sentences.sort(key=lambda x: x[-1], reverse=True)
    # sum the fitness values
    total_fitness = sum([sentence[-1] for sentence in sentences])
    # keep the top sentence
    selected_sentences = sentences[:1]
    # for every other sentence
    for sentence in sentences[1:]:
        # calculate the probability of being selected
        prob = sentence[-1] + 1 / (total_fitness + 1)
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
    
  
    
test_sentences = generate_sentences(NUM_SENTENCES, NUM_WORDS, NUM_LETTERS)

# print("Initial sentences:")
# display(test_sentences)

# create a wordset
wordset = make_word_set("words_sorted.txt")
corpus = make_corpus("hound_words.txt")


# calculate the fitness of each sentence
test_sentences = fitness(test_sentences, wordset, corpus)
# print("Initial sentences with fitness:")
# display(test_sentences)


# loop through the epochs
for i in range(EPOCHS):
    # breed the sentences
    test_sentences = crossover(test_sentences, corpus, CROSSOVER_RATE)
    # print("After crossover:")
    # display(test_sentences)
    # sentence mutation
    test_sentences = sentence_mutate(test_sentences, corpus, SENTENCE_MUTATION_RATE, SENTENCE_GROWTH_RATE, MAX_WORDS, NUM_LETTERS)
    # print("After sentence mutation:")
    # display(test_sentences)
    # word mutation
    test_sentences = word_mutate(test_sentences, wordset, WORD_MUTATION_RATE)
    # print("After word mutation:")
    # display(test_sentences)
    # adapt
    test_sentences = adapt(test_sentences, wordset, ADAPT_RATE)
    # print("After adapt:")
    # display(test_sentences)
    # calculate the fitness of each sentence
    test_sentences = selection(test_sentences)
    test_sentences = fitness(test_sentences, wordset, corpus)
    # display the sentences
    if i % 1000 == 0:
        print("Epoch", i + 1)
        display(test_sentences)   
print("Epoch", i + 1)
display(test_sentences)   
    


    