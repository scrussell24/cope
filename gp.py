import random
import operator
from math import sqrt
from typing import Any
from copy import deepcopy
from functools import partial, reduce

import hy

from ape import Population
from ape.tree import TreeNode
from ape.evaluate import evaluate as hy_eval


xs = [n/10. for n in range(-10, 10)]


class GPGenome:
    # These must be set
    depth = None
    branch = None
    functions = None
    terminals = None
    fn_term_ratio = 0.5
    mutation_rate = 0.1

    def __init__(self, *args, **kwargs):
        self.tree = args[0]
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        n = 20
        error_sum = 0
        for x in xs:
            error_sum += (((x**4 - x**3 - x**2 - x) - evaluate(self.tree, x))**2)/float(n)
        rmse = sqrt(error_sum)
        return rmse

    @classmethod
    def mate(cls, mom, dad):
        child, dad_tree = deepcopy(mom.tree), deepcopy(dad.tree)
        # crossover
        i = random.randint(0, len(child) - 1)
        dad_node = dad_tree.get(i)
        child.set(i, dad_node)
        # mutate
        def mutate(node):
            if random.random() < cls.mutation_rate:
                terminal = True if node.depth() == 0 else False
                return cls.rand_gene(terminal=terminal).val
            return node.data
        child.walk(mutate)
        return cls(child)

    @classmethod
    def rand(cls):
        return cls(cls.rand_tree(cls.depth))

    @classmethod
    def rand_gene(cls, terminal=False):
        if random.random() > cls.fn_term_ratio or terminal:
            return random.choice(cls.terminals)
        return random.choice(cls.functions)

    @classmethod
    def rand_tree(cls, depth):
        if depth > 0:
            gene = cls.rand_gene()
            children = [cls.rand_tree(depth - 1) for n in range(cls.branch)]
            return TreeNode(gene.val, children)
        else:
            gene = cls.rand_gene(terminal=True)
            return TreeNode(gene.val, [])

    def __str__(self):
        return f'fitness={self.fitness} {str(self.tree)}'


def evaluate(variables, tree, *args):
    points = {}
    for n in range(len(args)):
        points[variables[n]] = args[n]
        return hy_eval(points, tree)

class Primitive:
    def __init__(self, val):
        self.val = val


def first(i, j):
    return i


def second(i, j):
    return j


variables = ['x']
evaluate = partial(evaluate, variables)
terminals = [Primitive(var) for var in variables]
functions = [
    Primitive(operator.add),
    Primitive(operator.sub),
    Primitive(operator.mul),
    Primitive(first),
    Primitive(second)
]


class MyGPGenome(GPGenome):
    depth = 5
    branch = 2
    functions = functions
    terminals = terminals
    fn_term_ratio = 0.75
    mutation_rate = 0.25


def test_evolve():
    pop = Population(MyGPGenome, 1000)
    pop = pop.evolve(terminate=lambda x, y: y.get_chrm(0).fitness <= 0.001 or x > 100000)
    first = pop.get_chrm(0)
    print(first)
    print(first.fitness)


if __name__ == '__main__':
    test_evolve()
