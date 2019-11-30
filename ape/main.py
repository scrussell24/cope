from time import time
from random import random
from math import sqrt, pow, floor, log, ceil
from multiprocessing import Queue, Pool, Process, Pipe, cpu_count

from blist import sortedlist


def sorter(x):
    return x.fitness


def evaluator(chrm, waiting, nursery):
    while True:
        couples = waiting.get(True)
        kids = []
        for couple in couples:
            mom = couple[0]
            dad = couple[1]
            kids.append(chrm.mate(mom, dad))
        nursery.put(kids)


def manager(pop, terminate, waiting, nursery, pipe_to, batch_size):
    start_time = time()
    evals = 0
    while not terminate(evals, pop):
        if evals > 0 and evals % len(pop) == 0:
            total_time = time() - start_time
            evals_per_sec = evals / total_time
            print(f'{evals=}')
            print(f'{evals_per_sec=}')
            print(f'{waiting.qsize()=}')
            print(f'{nursery.qsize()=}')
            print(f'{pop[0].fitness=}')
        if not waiting.full() and not nursery.full():
            # try some batching
            couples = []
            for n in range(batch_size):
                mom = pop[pop.rand_index()]
                dad = pop[pop.rand_index()]
                couples.append((mom, dad))
            waiting.put(couples)
        if not nursery.empty():
            kids = nursery.get(False)
            for child in kids:
                pop.pop(len(pop) - pop.rand_index() - 1)
                pop.add(child)
            evals += batch_size
    print(f'Done {evals=}, {pop[0].fitness=}')
    pipe_to.send(pop)


class Population(sortedlist):

    def __init__(self, chrm, size):
        self.chrm = chrm
        super().__init__(
            [chrm.rand() for n in range(size)],
            key=sorter
        )

    def evolve(self, terminate, num_workers=cpu_count(), batch_size=None):
        if not batch_size:
            batch_size = ceil(log(len(self)) / 2.0)
            # batch_size = ceil(len(self)**(1/3.0))
            print(f'{batch_size=}')
        start_time = time()
        waiting = Queue(maxsize=2*num_workers)
        nursery = Queue(maxsize=2*num_workers)
        pipe_to, pipe_from = Pipe()
        print(f'{num_workers=}')
        pool = Pool(num_workers, evaluator, (self.chrm, waiting, nursery))
        mgr = Process(target=manager, args=(self, terminate, waiting, nursery, pipe_to, batch_size))
        mgr.start()
        new_pop = None
        while not new_pop:
            new_pop = pipe_from.recv()
        total_sec = time() - start_time
        total_min = total_sec / 60
        print(f'{total_sec=}')
        print(f'{total_min=}')
        return new_pop

    def sync_evolve(self, terminate):
        start_time = time()
        gen_start = time()
        gen = 0
        evals = 0
        while not terminate(evals := evals + 1, self):
            if evals % len(self) == 0:
                gen_total = time() - gen_start
                gen_start = time()
                evals_per_sec = len(self) / gen_total
                print(f'{gen=}')
                print(f'{gen_total=}')
                print(f'{evals=}')
                print(f'{evals_per_sec=}')
                print(f'{self[0].fitness=}')
                gen += 1
            mom = self[self.rand_index()]
            dad = self[self.rand_index()]
            child = self.chrm.mate(mom, dad)
            self.pop(len(self) - self.rand_index() - 1)
            self.add(child)
        total_sec = time() - start_time
        total_min = total_sec / 60
        print(f'{total_sec=}')
        print(f'{total_min=}')
        return self

    def rand_index(self):
        ex = 32 * log(len(self))
        return floor(len(self) * pow(random(), ex))

    def __str__(self):
        s = ""
        for n in self:
            s += str(n) + '\n'
        return s
