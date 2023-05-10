import datetime
import random
import unittest

import genetic

def get_fitness(guess, target):
    # simply count the number of matches between the guess and the target
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)

def display(candidate, startTime):

    timeDiff = datetime.datetime.now() - startTime
    # print the guess, the fitness, and the time taken
    print("{}\t{}\t{}".format(candidate.Genes, candidate.Fitness, timeDiff))


class GuessLettersTests(unittest.TestCase):
    geneset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

    def test_Hello_World(self):
        target = "Hello World!"
        self.guess_letters(target)

    def test_Sherlock(self):
        target = """Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent occasions when he was up all night, was seated at the breakfast table."""
        self.guess_letters(target)

    def guess_letters(self, target):   
        
        startTime = datetime.datetime.now()

        # helper functions nested inside the guess_letters function to have access to the target and startTime variables
        def fnGetFitness(genes):
            return get_fitness(genes, target)
        
        def fnDisplay(candidate):
            display(candidate, startTime)

        optimalFitness = len(target)
        best = genetic.get_best(fnGetFitness, len(target), optimalFitness, self.geneset, fnDisplay)
        self.assertEqual(best.Genes, target)

    def test_Random(self):
        length = 150
        target = ''.join(random.choice(self.geneset) for _ in range(length))
        self.guess_letters(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test_Random)

if __name__ == '__main__':
    unittest.main()



