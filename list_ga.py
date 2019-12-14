from functools import reduce

from ape import Population
from ape.genomes import BListGenome


class MyListGenome(BListGenome):
    length = 1000
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * self.length - reduce(lambda x, y: x + y, self.gene_list)


def test_evolve():
    pop = Population(MyListGenome, 1000)
    stats = pop.evolve(terminate=lambda x, y: y.get(0).fitness <= 0 or x > 1000000)
    print(stats)


if __name__ == '__main__':
    test_evolve()
