from time import time
from functools import reduce
from random import randint, random, choice

from blist import blist

from ape import Population


POP_SIZE = 1000
CHRM_LENGTH = 1000
MUTATION_RATE = 0.25
GENE_SET = range(10)
MAX_EVALS = 1000000


class Chromosome:
    mutation_rate = MUTATION_RATE
    length = CHRM_LENGTH
    gene_set = GENE_SET

    def __init__(self, *args, **kwargs):
        self.genome = blist(args[0])
        self.fitness = 9 * self.length - reduce(lambda x, y: x + y, self.genome)

    @classmethod
    def mate(cls, mom, dad):
        # crossover
        i = randint(0, cls.length - 1)
        new = blist(mom.genome[0:i] + dad.genome[i:cls.length])
        # mutate
        if random() < cls.mutation_rate:
            i = randint(0, cls.length - 1)
            new[i] = choice(cls.gene_set)
        return cls(new)

    @classmethod
    def rand(cls):
        return cls([choice(cls.gene_set) for n in range(cls.length)])

    def __str__(self):
        return f'{self.fitness=} {str(self.genome)}'


def test_evolve():
    pop = Population(Chromosome, POP_SIZE)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > MAX_EVALS)
    #pop.evolve(terminate=lambda x, y: y[0].fitness <= 0 or x > MAX_EVALS)
    first = pop[0]
    fitness = first.fitness
    assert True


if __name__ == '__main__':
    test_evolve()
