# geneSet = "abc"
geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

# target = "Hello World!"
target = """Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent occasions when he was up all night, was seated at the breakfast table."""
import random

def generate_parent(length):

    # start with an empty list
    genes = []
    
    while len(genes) < length:
        print(genes)

        # sampleSize is the number of genes to be added to the list
        # length is the minimum of:
        #   1. the desired length of the list - the number of genes already in the list
        #   2. the length of the geneSet
        # so if desired length is less than the length of the geneSet, then sampleSize is the desired length and it will be filled randomly without duplicates
        # if desired length is greater than the length of the geneSet, then sampleSize is the length of the geneSet, and it will be filled with the geneset repeated
        # if geneSet = "abc" and desired length is 6, then sampleSize is 3 and the list will be filled ie "a b c b c a"
        sampleSize = min(length - len(genes), len(geneSet))
        
        # extend the list with a random sample of the geneSet
        genes.extend(random.sample(geneSet, sampleSize))
    
    # return the list as a string1
    return ''.join(genes)

print(generate_parent(12))

def get_fitness(guess):
    # simply count the number of matches between the guess and the target
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)

def mutate(parent):
    # pick a random index in the parent string
    index = random.randrange(0, len(parent))
    # make the parent string back into a list
    childGenes = list(parent)
    # pick two random genes from the geneSet
    newGene, alternate = random.sample(geneSet, 2)
    # if the gene at the random index is the same as the first random gene, then replace it with the second random gene
    # otherwise replace it with the first random gene
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    # return the child as a string
    return ''.join(childGenes)

import datetime

def display(guess):
    timeDiff = datetime.datetime.now() - startTime
    # fitness is the number of matches between the guess and the target
    fitness = get_fitness(guess)
    # print the guess, the fitness, and the time taken
    print("{}\t{}\t{}".format(guess, fitness, str(timeDiff)))

random.seed()
# startTime is the time the program started
startTime = datetime.datetime.now()
# initialize bestParent to a random string
bestParent = generate_parent(len(target))
# initialize bestFitness to the fitness of bestParent
bestFitness = get_fitness(bestParent)
display(bestParent)

# loop until the fitness of the bestParent is equal to the length of the target
while True:
    # initialize child to the mutated bestParent
    child = mutate(bestParent)
    # initialize childFitness to the fitness of the child
    childFitness = get_fitness(child)
    # if there is no improvement in the fitness of the child over the fitness of the bestParent 
    if bestFitness >= childFitness:
        # continue to the next iteration of the loop
        continue
    display(child)
    # otherwise, if the fitness of the child is equal to the length of the target
    if childFitness == len(target):
        # then the child is the solution, so break out of the loop
        break
    # otherwise, the child is the new bestParent
    bestFitness = childFitness
    bestParent = child
    
