import operator
from math import sqrt
from typing import Any
from copy import deepcopy
from functools import partial
from dataclasses import dataclass
from random import random, randint, choice

import hy

from ape import Population
from ape.tree import TreeNode
from ape.evaluate import evaluate as hy_eval


class GPGenome:
    # These must be set
    depth = None
    functions = None
    terminals = None
    fn_term_ratio = 0.5
    mutation_rate = 0.1

    def __init__(self, *args, **kwargs):
        self.tree = args[0]
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        n = 10
        xs = [randint(0, 10) for n in range(n)]
        ys = [randint(0, 10) for n in range(n)]
        error_sum = 0
        for x in xs:
            for y in ys:
                error_sum += ((((4 * x) + 7) - evaluate(self.tree, x, y))**2)/float(n)
        rmse = sqrt(error_sum)
        return rmse

    @classmethod
    def mate(cls, mom, dad):
        child, dad_tree = deepcopy(mom.tree), deepcopy(dad.tree)
        # crossover
        i = randint(0, len(child) - 1)
        j = randint(0, len(dad_tree) - 1)
        dad_node = dad_tree.get(j)
        child.set(i, dad_node)
        # mutate
        if random() < cls.mutation_rate:
            i = randint(0, len(child) - 1)
            depth = child.get(i).depth()
            gene = cls.rand_tree(depth)
            child.set(i, gene)
        return cls(child)

    @classmethod
    def rand(cls):
        return cls(cls.rand_tree(cls.depth))

    @classmethod
    def rand_tree(cls, depth):
        if depth > 0 and random() < cls.fn_term_ratio:
            # choose a function
            primitive = choice(cls.functions)
            mn = primitive.min_args
            mx = primitive.max_args
            num_children = randint(mn, mx)
            children = [cls.rand_tree(depth - 1) for n in range(num_children)]
            return TreeNode(primitive.fn, children)
        else:
            # choose a terminal
            primitive = choice(cls.terminals)
            return TreeNode(primitive.terminal, [])

    def __str__(self):
        return f'fitness={self.fitness} {str(self.tree)}'


def evaluate(variables, tree, *args):
    points = {}
    for n in range(len(args)):
        points[variables[n]] = args[n] 
    return hy_eval(points, tree)


@dataclass
class FunctionPrimitive:
    fn: Any
    min_args: int
    max_args: int


@dataclass
class TerminalPrimitive:
    terminal: Any


evaluate = partial(evaluate, ['x', 'y'])
terminals = [TerminalPrimitive(var) for var in ['x', 'y']] + [TerminalPrimitive(n) for n in range(9)]
functions = [
    FunctionPrimitive(operator.add, 2, 2),
    FunctionPrimitive(operator.sub, 2, 2),
    FunctionPrimitive(operator.mul, 2, 2)
]


class MyGPGenome(GPGenome):
    depth = 3
    functions = functions
    terminals = terminals
    fn_term_ratio = 0.75
    mutation_rate = 0.25


def test_evolve():
    pop = Population(MyGPGenome, 1000)
    pop = pop.sync_evolve(terminate=lambda x, y: y[0].fitness <= 0 or x > 100000)
    first = pop[0]
    print(first)
    print(first.fitness)
    print(first.tree.depth())


if __name__ == '__main__':
    test_evolve()
