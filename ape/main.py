from time import time
from random import random
from math import sqrt, pow, floor, log
from multiprocessing import Queue, Pool, Process, cpu_count

from blist import sortedlist


class Population(sortedlist):

    def __init__(self, chrm, size):

        def sorter(x):
            return x.fitness

        self.chrm = chrm
        super().__init__(
            [chrm.rand() for n in range(size)],
            key=sorter
        )

    def evaluator(self, waiting, nursery):
        while True:
            item = waiting.get(True)
            mom = item[0]
            dad = item[1]
            child = self.chrm.mate(mom, dad)
            nursery.put(child)

    def manager(self, terminate, waiting, nursery):
        start_time = time()
        evals = 0
        while not terminate(evals, self):
            if evals > 0 and evals % len(self) == 0:
                total_time = time() - start_time
                evals_per_sec = evals / total_time
                print(f'{evals=}')
                print(f'{evals_per_sec=}')
                print(f'{waiting.qsize()=}')
                print(f'{nursery.qsize()=}')
                print(f'{self[0].fitness=}')
            if not waiting.full() and not nursery.full():
                mom = self[self.rand_index()]
                dad = self[self.rand_index()]
                waiting.put((mom, dad))
            if not nursery.empty():
                child = nursery.get(False)
                self.pop(len(self) - self.rand_index() - 1)
                self.add(child)
                evals += 1
        print(f'{evals=}, {self[0].fitness=}')

    def evolve(self, terminate, num_workers=cpu_count()):
        start_time = time()
        waiting = Queue(maxsize=2*num_workers)
        nursery = Queue(maxsize=2*num_workers)
        print(f'{num_workers=}')
        pool = Pool(num_workers, self.evaluator, (waiting, nursery))
        mgr = Process(target=self.manager, args=(terminate, waiting, nursery))
        mgr.start()
        mgr.join()
        total_sec = time() - start_time
        total_min = total_sec / 60
        print(f'{total_sec=}')
        print(f'{total_min=}')

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
        return evals

    def rand_index(self):
        ex = 32 * log(len(self))
        return floor(len(self) * pow(random(), ex))
