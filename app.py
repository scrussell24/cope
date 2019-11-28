from ape import Population
from ape.genomes import list_genome


def test_evolve():
    genome = list_genome(
        length=1000,
        genes=range(10),
        mutation_rate=0.25
    )
    pop = Population(genome, 1000)
    #pop.sync_evolve(terminate=lambda evals, pop: pop[0].fitness <= 0 or evals > 1000000)
    pop.evolve(terminate=lambda x, y: y[0].fitness <= 0 or x > 1000000)
    first = pop[0]
    fitness = first.fitness
    assert True


if __name__ == '__main__':
    test_evolve()
