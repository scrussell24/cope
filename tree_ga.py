from functools import reduce

from ape import Population
from ape.genomes import TreeGenome


class MyTreeGenome(TreeGenome):
    depth = 5
    branch = 2
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * len(self.tree) - self.tree.reduce(lambda x, y: x.data + y, 0)


def test_evolve():
    pop = Population(MyTreeGenome, 10000)
    #pop = pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    pop = pop.evolve(terminate=lambda x, y: y[0].fitness <= 0 or x > 1000000)
    first = pop[0]
    print(first.fitness)

if __name__ == '__main__':
    test_evolve()
