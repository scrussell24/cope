from random import randint, random
from functools import reduce

from blist import blist

from ape import Population


def test_evolve():
    POP_SIZE = 1000
    CHRM_LENGTH = 1000
    MUTATION_RATE = 0.25
    MAX_EVALS = 1000000

    class Chromosome(blist):
        mutation_rate = MUTATION_RATE
        length = CHRM_LENGTH
        rand_gene = lambda: randint(0, 9)
        rand_index = lambda: randint(0, CHRM_LENGTH - 1)
        fitness = None

        @classmethod
        def rand(cls):
            new = cls([cls.rand_gene() for n in range(cls.length)])
            new._set_fitness()
            return new

        def mate(self, dad):
            # crossover
            cls = self.__class__
            i = cls.rand_index()
            new = cls(self[0:i] + dad[i:cls.length])
            # mutate
            if random() < cls.mutation_rate:
                i = cls.rand_index()
                new[i] = cls.rand_gene()
            # set_fitness
            new._set_fitness()
            return new

        def _set_fitness(self):
            # select for 9's
            self.fitness = 9 * self.length - reduce(lambda x, y: x + y, self)

    pop = Population(Chromosome, POP_SIZE)
    evals = pop.evolve(terminate=lambda x, y: y[0].fitness <= 10 or x > MAX_EVALS)
    first = pop[0]
    fitness = first.fitness
    print(first, fitness, evals)
    assert True
