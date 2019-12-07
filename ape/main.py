from time import time
from random import random, randint
from math import sqrt, pow, floor, log, ceil
from multiprocessing import Queue, Pool, Process, Pipe, cpu_count

from blist import sorteddict


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
            print(f'evals={evals}')
            print(f'evals_per_sec={evals_per_sec}')
            print(f'waiting_qsize={waiting.qsize()}')
            print(f'nursery_qsize={nursery.qsize()}')
            print(f'fitness={pop.get_chrm(0).fitness}')
        if not waiting.full() and not nursery.full():
            # try some batching
            couples = []
            for n in range(batch_size):
                mom = pop.get_chrm(pop.rand_index())
                dad = pop.get_chrm(pop.rand_index())
                couples.append((mom, dad))
            waiting.put(couples)
        if not nursery.empty():
            kids = nursery.get(False)
            for child in kids:
                pop.pop_chrm(len(pop) - pop.rand_index() - 1)
                pop.add_chrm(child)
            evals += batch_size
    print(f'Done evals={evals}, fitness={pop.get_chrm(0).fitness}')
    pipe_to.send(pop)


class Population(sorteddict):

    def __init__(self, chrm, size):
        super().__init__()
        self.chrm = chrm
        chrms = [chrm.rand() for n in range(size)]
        for chrm in chrms:
            self.add_chrm(chrm)

    def evolve(self, terminate, num_workers=cpu_count(), batch_size=None):
        if not batch_size:
            batch_size = ceil(log(len(self)) / 2.0)
        print(f'batch_size={batch_size}')
        start_time = time()
        waiting = Queue(maxsize=2*num_workers)
        nursery = Queue(maxsize=2*num_workers)
        pipe_to, pipe_from = Pipe()
        print(f'num_workers={num_workers}')
        pool = Pool(num_workers, evaluator, (self.chrm, waiting, nursery))
        mgr = Process(target=manager, args=(self, terminate, waiting, nursery, pipe_to, batch_size))
        mgr.start()
        new_pop = None
        while not new_pop:
            new_pop = pipe_from.recv()
        total_sec = time() - start_time
        total_min = total_sec / 60
        print(f'total_sec={total_sec}')
        print(f'total_min={total_min}')
        return new_pop

    def sync_evolve(self, terminate):
        start_time = time()
        gen_start = time()
        gen = 0
        evals = 0
        while not terminate(evals, self):
            if evals % len(self) == 0:
                gen_total = time() - gen_start
                gen_start = time()
                evals_per_sec = len(self) / gen_total
                print(f'gen={gen}')
                print(f'gen_totals={gen_total}')
                print(f'evals={evals}')
                print(f'evals_per_sec={evals_per_sec}')
                print(f'fitness={self.get_chrm(0).fitness}')
                gen += 1
            mom = self.get_chrm(self.rand_index())
            dad = self.get_chrm(self.rand_index())
            child = self.chrm.mate(mom, dad)
            self.pop_chrm(len(self) - self.rand_index() - 1)
            self.add_chrm(child)
            evals += 1
        total_sec = time() - start_time
        total_min = total_sec / 60
        print(f'total_sec={total_sec}')
        print(f'total_min={total_min}')
        return self

    def rand_index(self):
        ex = 32 * log(len(self))
        return floor(len(self) * pow(random(), ex))

    def pop_chrm(self, index):
        key = self._get_key(index)
        chrm = self[key].pop(randint(0, len(self[key]) - 1))
        if len(self[key]) == 0:
            del self[key]
        return chrm

    def get_chrm(self, index):
        key = self._get_key(index)
        return self[key][randint(0, len(self[key]) - 1)]

    def add_chrm(self, chrm):
        if self.get(chrm.fitness) == None:
            self[chrm.fitness] = [chrm]
        else:
            self[chrm.fitness].append(chrm)

    def _get_key(self, index):
        for k, v in self.items():
            index = index - len(v)
            if index <= 0:
                return k

    def __len__(self):
        size = 0
        for k, v in self.items():
            size += len(v)
        return size

    def __str__(self):
        s = ""
        for k, v in self.items():
            for n in list(v):
                s += str(n) + '\n'
        return s
