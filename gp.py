import random
import operator
from math import sqrt
from copy import deepcopy
from functools import partial

import hy

from ape import Population
from ape.tree import TreeNode
from ape.evaluate import evaluate as hy_eval


variables = ['x', 'y']
intervals = [n/10. for n in range(-10, 10)]


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
        self.compiled = self.compile(args[0])

    @classmethod
    def compile(cls, tree):
        new_tree = TreeNode(None, None)
        if callable(tree.data):
            # first compile children
           
            # reaplce with first child
            if tree.data.__name__ == 'first':
                new_tree.data = tree.children[0].data
                new_tree.children = [cls.compile(c) for c in tree.children[0].children]
            # replace with second child
            elif tree.data.__name__ == 'second':
                new_tree.data = tree.children[1].data
                new_tree.children = [cls.compile(c) for c in tree.children[1].children]
            else:
                try:
                    # try executing the function
                    new_tree.data = tree.data(tree.children[0], tree.children[1])
                    new_tree.children = []
                except Exception as err:
                    new_tree.data = tree.data
                    new_tree.children = [cls.compile(c) for c in tree.children]
        else:
            # not a function so get rid of children
            new_tree.data = tree.data
            new_tree.children = []
        return new_tree

    def calc_fitness(self):
        error_sum = 0
        num_samples = len(intervals)**len(variables)
        for x in intervals:
            for y in intervals:
                error_sum += (((x**2 - y**2) - evaluate(self.tree, x, y))**2)/float(num_samples)
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
        return f'fitness={self.fitness} {str(self.compiled)}'


def evaluate(variables, tree, *args):
    points = {}
    for n in range(len(args)):
        points[variables[n]] = args[n]
    return hy_eval(points, tree)

class Primitive:
    def __init__(self, val):
        self.val = val


def first(x, y):
    return x


def second(x, y):
    return y


evaluate = partial(evaluate, variables)
terminals = [Primitive(var) for var in variables] + [Primitive(n) for n in range(10)]
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
    pop = Population(MyGPGenome, 10000)
    pop = pop.evolve(terminate=lambda x, y: y.get(0).fitness <= 0.001 or x > 1000000)
    first = pop.get(0)
    print(first.tree)
    print(first)
    print(first.fitness)


if __name__ == '__main__':
    test_evolve()
