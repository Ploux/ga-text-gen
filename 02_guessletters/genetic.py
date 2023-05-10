import random
import statistics
import sys
import time


def _generate_parent(length, geneSet, get_fitness):

    # start with an empty list
    genes = []
    
    while len(genes) < length:
        

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

        # convert the list to a string
    genes = ''.join(genes)
    # calculate the fitness of the string
    fitness = get_fitness(genes)
    # return a Chromosome object with the string and the fitness
    return Chromosome(genes, fitness)
    

    
    # return the list as a string
    return ''.join(genes)

def _mutate(parent, geneSet, get_fitness):
    # pick a random index in the parent string
    index = random.randrange(0, len(parent.Genes))
    # make the parent string back into a list
    childGenes = list(parent.Genes)
    # pick two random genes from the geneSet
    newGene, alternate = random.sample(geneSet, 2)
    # if the gene at the random index is the same as the first random gene, then replace it with the second random gene
    # otherwise replace it with the first random gene
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    # convert the list back to a string
    genes = ''.join(childGenes)
    # calculate the fitness of the child
    fitness = get_fitness(genes)
    # return a new Chromosome object with the new genes and fitness
    return Chromosome(genes, fitness)



def get_best(get_fitness, targetLen, optimalFitness, geneSet, display):
    """
    get_fitness: the function called to request the fitness for a guess
    targetLen: number of genes to use when creating a new gene sequence
    optimalFitness: the fitness at which the program should stop running
    geneSet: the set of genes to use when creating or mutating a gene sequence
    display: the function called to display or report each improvement found
    """
    random.seed()
    # startTime is the time the program started
    # initialize bestParent to a random string
    bestParent = _generate_parent(targetLen, geneSet, get_fitness)
    display(bestParent)

    # if the fitness of the bestParent is equal to the optimalFitness exit the loop and return the bestParent
    if bestParent.Fitness >= optimalFitness:
        return bestParent

    # loop until the fitness of the bestParent is equal to the optimalFitness
    while True:
        # initialize child to the mutated bestParent
        child = _mutate(bestParent, geneSet, get_fitness)
        # initialize childFitness to the fitness of the child
        if bestParent.Fitness >= child.Fitness:
            # continue to the next iteration of the loop
            continue
        display(child)
        # otherwise, if the fitness of the child is equal to the optimalFitness
        if child.Fitness >= optimalFitness:
            # then the child is the solution, so break out of the loop and return the child
            return child
        bestParent = child
    
class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

    
class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        for i in range(100):
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            timings.append(seconds)
            mean = statistics.mean(timings)
            print("{} {:3.2f} {:3.2f}".format(1 + i, mean, statistics.stdev(timings, mean) if i > 1 else 0))

