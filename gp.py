import random
import operator
from math import sqrt
from typing import Any
from copy import deepcopy
from dataclasses import dataclass
from functools import partial, reduce

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
        n = 20
        xs = [n/10. for n in range(-10, 10)]
        ys = [n/10. for n in range(-10, 10)]
        error_sum = 0
        for x in xs:
            for y in ys:
                error_sum += (((x**3 - x**1) - evaluate(self.tree, x))**2)/float(n)
        rmse = sqrt(error_sum)
        return rmse

    @classmethod
    def mate(cls, mom, dad):
        child, dad_tree = deepcopy(mom.tree), deepcopy(dad.tree)
        # crossover
        i = random.randint(0, len(child) - 1)
        j = random.randint(0, len(dad_tree) - 1)
        dad_node = dad_tree.get(j)
        child.set(i, dad_node)
        # mutate
        if random.random() < cls.mutation_rate:
            i = random.randint(0, len(child) - 1)
            depth = child.get(i).depth()
            gene = cls.rand_tree(depth)
            child.set(i, gene)
        return cls(child)

    @classmethod
    def rand(cls):
        return cls(cls.rand_tree(cls.depth))

    #@classmethod
    #def rand_gene(cls):


    @classmethod
    def rand_tree(cls, depth):
        if depth > 0 and random.random() < cls.fn_term_ratio:
            # choose a function
            primitive = random.choice(cls.functions)
            mn = primitive.min_args
            mx = primitive.max_args
            num_children = random.randint(mn, mx)
            children = [cls.rand_tree(depth - 1) for n in range(num_children)]
            return TreeNode(primitive.fn, children)
        else:
            # choose a terminal
            primitive = random.choice(cls.terminals)
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


def first(x, y):
    return x


def second(x, y):
    return y


variables = ['x']
evaluate = partial(evaluate, variables)
terminals = [TerminalPrimitive(var) for var in variables]
functions = [
    FunctionPrimitive(operator.add, 2, 2),
    FunctionPrimitive(operator.sub, 2, 2),
    FunctionPrimitive(operator.mul, 2, 2),
    FunctionPrimitive(first, 2, 2),
    FunctionPrimitive(second, 2, 2)
]


class MyGPGenome(GPGenome):
    depth = 6
    functions = functions
    terminals = terminals
    fn_term_ratio = 0.75
    mutation_rate = 0.1


def test_evolve():
    pop = Population(MyGPGenome, 1000)
    pop = pop.evolve(terminate=lambda x, y: y[0].fitness <= 0.001 or x > 100000)
    first = pop[0]
    print()
    print(first)
    print(first.fitness)
    print(first.tree.depth())


if __name__ == '__main__':
    test_evolve()
