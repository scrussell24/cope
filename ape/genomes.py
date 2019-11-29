from copy import deepcopy
from random import randint, random, choice

from blist import blist

from ape.tree import TreeNode


class ListGenome:
    # These must be set
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


class TreeGenome:
    # These must be set
    depth = None
    branch = None
    genes = None
    mutation_rate = None

    def __init__(self, *args, **kwargs):
        self.tree = args[0]
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        return None

    @classmethod
    def mate(cls, mom, dad):
        # crossover
        child, dad_tree = deepcopy(mom.tree), deepcopy(dad.tree)
        i = randint(0, len(dad_tree) - 1)
        dad_node = dad_tree.get(i)
        child.set(i, dad_node)
        # mutate
        if random() < cls.mutation_rate:
            i = randint(0, len(child) - 1)
            child.get(i).data = choice(cls.genes)
        return cls(child)

    @classmethod
    def rand(cls):
        return cls(cls.rand_tree(cls.depth))

    @classmethod
    def rand_tree(cls, depth):
        children = []
        if depth > 0:
            children = [cls.rand_tree(depth - 1) for n in range(cls.branch)]
        return TreeNode(choice(cls.genes), children)


    def __str__(self):
        return f'{self.fitness=} {str(self.tree)}'
