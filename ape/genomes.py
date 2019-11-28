from random import randint, random, choice

from blist import blist


class ListGenome:
    # These must be set
    # see list_genome factory function
    length = None
    genes = None
    mutation_rate = None

    def __init__(self, *args, **kwargs):
        self.gene_list = args[0]
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        return None

    @classmethod
    def mate(cls, mom, dad):
        # crossover
        i = randint(0, cls.length - 1)
        new = mom.gene_list[0:i] + dad.gene_list[i:cls.length]
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


class BListGenome(ListGenome):

    def __init__(self, *args, **kwargs):
        self.gene_list = blist(args[0])
        self.fitness = self.calc_fitness()


# class TreeGenome: pass
