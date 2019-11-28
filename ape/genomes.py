from time import time
from functools import reduce
from random import randint, random, choice

from blist import blist


class ListGenome:
    # These must be set
    # see list_genome factory function
    length = None
    genes = None
    fitness_fn = None
    mutation_rate = None

    def __init__(self, *args, **kwargs):
        self.gene_list = blist(args[0])
        self.fitness = self.fitness_fn()

    @classmethod
    def mate(cls, mom, dad):
        # crossover
        i = randint(0, cls.length - 1)
        new = blist(mom.gene_list[0:i] + dad.gene_list[i:cls.length])
        # mutate
        if random() < cls.mutation_rate:
            i = randint(0, cls.length - 1)
            new[i] = choice(cls.genes)
        return cls(new)

    @classmethod
    def rand(cls):
        return cls([choice(cls.genes) for n in range(cls.length)])

    def __str__(self):
        return f'{self.fitness=} {str(self.gene_list)}'


def list_genome(length, genes, fitness, mutation_rate):
    ListGenome.genes = genes
    ListGenome.length = length
    ListGenome.fitness_fn = fitness
    ListGenome.mutation_rate = mutation_rate
    return ListGenome
