from random import random
from math import sqrt, pow, floor, log
import multiprocessing

from blist import sortedlist


class Population(sortedlist):

    def __init__(self, chrm, size):
        super().__init__(
            [chrm.rand() for n in range(size)],
            key=lambda x: x.fitness
        )

    def evolve(self, terminate, workers=multiprocessing.cpu_count()):
        evals = 0
        while not terminate(evals, self):
            mom = self[self.rand_index()]
            dad = self[self.rand_index()]
            child = mom.mate(dad)
            self.pop(len(self) - self.rand_index() - 1)
            self.add(child)
            evals += 1
        return evals

    def rand_index(self):
        ex = 8 * log(len(self))
        return floor(len(self) * pow(random(), ex))
