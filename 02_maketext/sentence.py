import random
import datetime


EPOCHS = 1000
CROSSOVER_RATE = 0.1
SENTENCE_MUTATION_RATE = 1
WORD_MUTATION_RATE = 1
ADAPT_RATE = 1

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
        # create a set of the words that are 3 or more letters long, converting them to lowercase
        wordset = set([word.lower() for word in words if len(word) > 2])
        # add the words 'a' and 'i' to the wordset
        wordset.add('a')
        wordset.add('i')
        # add the two letter word list to the wordset
        two_letters = ["as", "to", "be", "in", "by", "is", "it", "at", "of", "or", "on", "an", "us", "if", "my", "do", "no", "he", "up", "so", "pm", "am", "me", "re", "go", "cd", "tv", "pc", "id", "oh", "ma", "mr", "ms", "dr", "os", "ex", "ft", "vs", "ie", "eg"]
        for word in two_letters:
            wordset.add(word)
               
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
    # loop through each sentence
    for sentence in sentences:
        fitness = 0
        # loop through each word in the sentence
        for i in range(len(sentence) - 1):
            # if the word is in the wordset
            if sentence[i] in wordset:
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
                # if the sentence does not have a fitness value = len(sentence) - 1
                if len(sentence) < 21 and sentence[-1] != len(sentence) - 1:
                    # add a 5 letter word at the end (before the fitness value)
                    word = ''
                    for i in range(5):
                        # add a random letter to the word
                        word += random.choice(geneSet)
                    sentence.insert(-1, word)
            else:
                # if the sentence has 3 or more words
                if len(sentence) > 3 and sentence[-1] != len(sentence) - 1:
                    # remove the last word
                    sentence.pop(-2)
    return sentences

def word_mutate(sentences, wordset, WORD_MUTATION_RATE):
    for sentence in sentences:
        for i in range(len(sentence) - 1):
            # if the word is not in the wordset
            if sentence[i] not in wordset:
                # flip a coin, if heads add a letter, if tails remove a letter
                if random.random() < WORD_MUTATION_RATE:
                    # flip a coin, if heads add a letter, if tails remove a letter
                    if len(sentence[i]) < 15 and random.random() < 0.5:
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
    
   
    
test_sentences = sentences(20, 10, 5)

# append a sentence with some real words
# test_sentences.append(['hello', 'wooor', 'sasrt', 'bdrr', 'wfcra', 'ttt', 'qq', 'asruuul', 'jarfer', 'pppo', 0])
# test_sentences.append(['hello', 'wooo', 'sasrt', 'bdrr', 0])

print("Initial sentences:")
display(test_sentences)

# create a wordset
wordset = makedict("02_maketext/american-english.txt")

# calculate the fitness of each sentence
test_sentences = fitness(test_sentences, wordset)
print("Initial sentences with fitness:")
display(test_sentences)

"""
# test adaptation
test_sentences = adapt(test_sentences, wordset, 1)
print("After adaptation:")
display(test_sentences)
"""

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
    test_sentences = fitness(test_sentences, wordset)
    # display the sentences
    print("Epoch", i + 1)
    display(test_sentences)   
    

# create a wordset and print the first 100 words, the length, and save it to a file
# wordset = makedict("02_maketext/american-english.txt", True)
# print(list(wordset)[:100])
# print(len(wordset))

    