from functools import reduce

from ape import Population
from ape.genomes import ListGenome


class MyListGenome(ListGenome):
    length = 10
    genes = range(10)
    mutation_rate = 0.25

    def calc_fitness(self):
        return 9 * self.length - reduce(lambda x, y: x + y, self.gene_list)


def test_sync_evolve():
    pop = Population(MyListGenome, 10)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    first = pop[0]
    assert first.fitness == 0


if __name__ == '__main__':
    test_sync_evolve()
