from functools import reduce

from ape import Population
from ape.genomes import list_genome


def fitness(genome):
    return 9 * genome.length - reduce(lambda x, y: x + y, genome.gene_list)


def test_sync_evolve():
    genome = list_genome(
        length=10,
        genes=range(10),
        fitness=fitness,
        mutation_rate=0.25
    )
    pop = Population(genome, 1000)
    pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    first = pop[0]
    assert first.fitness == 0


if __name__ == '__main__':
    test_sync_evolve()
