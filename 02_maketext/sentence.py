import random
import datetime


EPOCHS = 5000
NUM_SENTENCES = 50
NUM_WORDS = 10
NUM_LETTERS = 5
MAX_WORDS = 20
CROSSOVER_RATE = 0.1
SENTENCE_MUTATION_RATE = 1
WORD_MUTATION_RATE = 1
WORD_GROWTH_RATE = 0.75 # 0.5 means words have equal chance to grow or shrink
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
def fitness(sentences, wordset):
    # initialize the fitness
    # loop through each sentence
    for sentence in sentences:
        fitness = 0
        length = 0
        # loop through each word in the sentence
        for i in range(len(sentence) - 1):
            length += len(sentence[i])
            # if the word is in the wordset
            if sentence[i] in wordset:
                # add half length of the word to the fitness
                fitness += len(sentence[i])
        # add average length of words in the sentence
        # fitness += length/(len(sentence)-1)
        # update the fitness value of the sentence
        sentence[-1] = fitness
        # if two words in a row are the same, make fitness = 0
        for i in range(len(sentence) - 2):
            if sentence[i] == sentence[i + 1]:
                sentence[-1] = 0
                continue
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
    
# function to breed the sentences
def crossover(sentences, wordset, CROSSOVER_RATE):
    # randomize the order of the sentences
    random.shuffle(sentences)
    # go through each pair of sentences; for now assume even number of sentences
    for i in range(0, len(sentences), 2):
        # for the length of the shorter sentence
        for j in range(min(len(sentences[i])-1, len(sentences[i + 1])-1)):
            # check the word at this position in each sentence
            # if they are both words, or neither are words, do nothing
            # if one is a word and the other is not, replace the non-word with the word
            if random.random() < CROSSOVER_RATE:
                if sentences[i][j] in wordset and sentences[i + 1][j] not in wordset:
                    sentences[i + 1][j] = sentences[i][j]
                elif sentences[i][j] not in wordset and sentences[i + 1][j] in wordset:
                    sentences[i][j] = sentences[i + 1][j]
    # return the sentences
    return sentences

def sentence_mutate(sentences, SENTENCE_MUTATION_RATE):
    for sentence in sentences:
        if random.random() < SENTENCE_MUTATION_RATE:
            # flip a coin, if heads add a word, if tails remove a word
            if random.random() < 0.5:
                # if the sentence does not exceed the max number of words and the fitness value is low enough
                if len(sentence) < MAX_WORDS and sentence[-1] < len(sentence) - 1:
                    # add a 5 letter word at the end (before the fitness value)
                    word = ''
                    for i in range(5):
                        # add a random letter to the word
                        word += random.choice(geneSet)
                    sentence.insert(-1, word)
            else:
                # if the sentence has 3 or more words
                if len(sentence) >= 4:
                    # remove a random word if it is not in the wordlist
                    word = random.choice(sentence[:-1])
                    if word not in wordset:
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
# make_dict('20k.txt')
wordset = make_word_set("words_sorted.txt")


# calculate the fitness of each sentence
test_sentences = fitness(test_sentences, wordset)
print("Initial sentences with fitness:")
display(test_sentences)


# loop through the epochs
for i in range(EPOCHS):
    # breed the sentences
    test_sentences = crossover(test_sentences, wordset, CROSSOVER_RATE)
    # print("After crossover:")
    # display(test_sentences)
    # sentence mutation
    test_sentences = sentence_mutate(test_sentences, SENTENCE_MUTATION_RATE)
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
    test_sentences = fitness(test_sentences, wordset)
    # display the sentences
    if i % 1000 == 0:
        print("Epoch", i + 1)
        display(test_sentences)   
print("Epoch", i + 1)
display(test_sentences)   
    


    