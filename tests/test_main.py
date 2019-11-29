from functools import reduce

from ape import Population
from ape.genomes import ListGenome, BListGenome, TreeGenome


class MyListGenome(ListGenome):
    length = 10
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * self.length - reduce(lambda x, y: x + y, self.gene_list)


def test_list_evolve():
    pop = Population(MyListGenome, 10)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    first = pop[0]
    assert first.fitness == 0


class MyBListGenome(BListGenome):
    length = 10
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * self.length - reduce(lambda x, y: x + y, self.gene_list)


def test_blist_evolve():
    pop = Population(MyBListGenome, 10)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    first = pop[0]
    assert first.fitness == 0


class MyTreeGenome(TreeGenome):
    depth = 3
    branch = 2
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * len(self.tree) - self.tree.reduce(lambda x, y: x.data + y, 0)


def test_tree_evolve():
    pop = Population(MyTreeGenome, 10)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    first = pop[0]
    assert first.fitness == 0
