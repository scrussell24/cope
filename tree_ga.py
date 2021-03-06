from functools import reduce

from cope import Population
from cope.genomes import TreeGenome


class MyTreeGenome(TreeGenome):
    depth = 5
    branch = 2
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * len(self.tree) - self.tree.reduce(lambda x, y: x.data + y, 0)


def test_evolve():
    pop = Population(MyTreeGenome, 1000)
    stats = pop.evolve(terminate=lambda x, y: y.get(0).fitness <= 0 or x > 1000000)
    print(stats)

if __name__ == '__main__':
    test_evolve()
