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
    pop = pop.sync_evolve(terminate=lambda x, y: y.get_chrm(0).fitness <= 0 or x > 1000000)
    first = pop.get_chrm(0)
    print(first.fitness)

if __name__ == '__main__':
    test_evolve()
