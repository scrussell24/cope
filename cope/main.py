from time import time
from random import random, randint
from math import pow, floor, log, ceil
from multiprocessing import Queue, Pool, Process, Pipe, cpu_count

from blist import sortedlist, blist


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
    gens = 0
    while not terminate(gens, pop):
        if evals > 0 and evals >= len(pop):
            total_time = time() - start_time
            gen = StatsGen(
                total_time,
                evals,
                pop.get(0).fitness,
                len(pop.pop_dict),
            )
            evals = 0
            gens += 1
            start_time = time()
            pipe_to.send(Message(MessageType.GEN, gen))
        if not waiting.full() and not nursery.full():
            couples = []
            for n in range(batch_size):
                mom = pop.get(pop.rand_index())
                dad = pop.get(pop.rand_index())
                couples.append((mom, dad))
            waiting.put(couples)
        if not nursery.empty():
            kids = nursery.get(False)
            for child in kids:
                pop.pop(len(pop) - pop.rand_index() - 1)
                pop.add(child)
            evals += batch_size
    else:
        total_time = time() - start_time
        gen = StatsGen(
            total_time,
            evals,
            pop.get(0).fitness,
            len(pop.pop_dict),
        )
        start_time = time()
        pipe_to.send(Message(MessageType.GEN, gen))
    pipe_to.send(Message(MessageType.DONE, pop))


class StatsGen:
    headers = [
        'elapsed time',
        'evals',
        'evals/sec',
        'best fitness',
        'fitness classes'
    ]

    def __init__(
            self,
            total_time,
            evaluations,
            best_fitness,
            fitness_classes
        ):
        self.time_elapsed = total_time
        self.evaluations = evaluations
        self.best_fitness = best_fitness
        self.fitness_classes = fitness_classes
    
    def __str__(self):
        s = ''
        s += str(self.time_elapsed) + ', '
        s += str(self.evaluations) + ', '
        s += str(self.evaluations / self.time_elapsed) + ', '
        s += str(self.best_fitness) + ', '
        s += str(self.fitness_classes)
        return s


class MessageType:
    DONE = 'done'
    GEN = 'gen'


class Message:

    def __init__(self, message_type, payload):
        self.type = message_type
        self.payload = payload


class Stats:

    def __init__(self, batch_size=1, num_workers=1):
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.generations = blist([])
        self.total_time = 0
        self.start_time = None

    def start(self, fn=None):
        self.start_time = time()
        if fn:
            fn(self)

    def end(self, fn=None):
        self.total_time = time() - self.start_time
        if fn:
            fn(self)
        else:
            # print(self)
            ...

    def add_gen(self, gen, fn=None):
        self.generations.append(gen)
        if fn:
            fn(self)
        else:
            # print(gen)
            ...

    def __str__(self):
        s = '# STATISTICS\n\n'
        s += '## GENERATIONS\n'
        s += '#, '
        for header in StatsGen.headers:
            s += str(header) + ', '
        s = s[:-2] + '\n'
        for i, gen in enumerate(self.generations):
            s += str(i) + ', ' + str(gen) + '\n'
        s += '\n'
        s += '* batch_size: ' + str(self.batch_size) + '\n'
        s += '* num_workers: ' + str(self.num_workers) + '\n'
        s += '* num_generations: ' + str(len(self.generations)) + '\n'
        s += '* total time: ' + str(self.total_time) + '\n\n'
        return s


class Population:

    def __init__(self, chrm, size):
        self.fitness_indeces = sortedlist([])
        self.pop_dict = dict()
        self.chrm = chrm
        self.size = size
        chrms = [chrm.rand() for n in range(size)]
        for chrm in chrms:
            self.add(chrm)

    def evolve(self, terminate, num_workers=cpu_count(), batch_size=None):
        if not batch_size:
            batch_size = ceil(log(len(self)) / 2.0)
        stats = Stats(batch_size=batch_size, num_workers=num_workers)
        stats.start()
        waiting = Queue(maxsize=2*num_workers)
        nursery = Queue(maxsize=2*num_workers)
        pipe_to, pipe_from = Pipe()
        pool = Pool(num_workers, evaluator, (self.chrm, waiting, nursery))
        mgr = Process(target=manager, args=(self, terminate, waiting, nursery, pipe_to, batch_size))
        mgr.start()
        new_pop = None
        while not new_pop:
            message = pipe_from.recv()
            if message.type == MessageType.DONE:
                new_pop = message.payload
                self.fitness_indeces = new_pop.fitness_indeces
                self.pop_dict = new_pop.pop_dict
            if message.type == MessageType.GEN:
                stats.add_gen(message.payload)
        stats.end()
        return stats

    def sync_evolve(self, terminate):
        stats = Stats()
        stats.start()
        gen_start = time()
        evals = 0
        while not terminate(evals, self):
            mom = self.get(self.rand_index())
            dad = self.get(self.rand_index())
            child = self.chrm.mate(mom, dad)
            self.pop(len(self) - self.rand_index() - 1)
            self.add(child)
            evals += 1

            if evals % len(self) == 0:
                gen_total = time() - gen_start
                gen_start = time()
                stats.add_gen(StatsGen(
                    gen_total,
                    len(self),
                    self.get(0).fitness,
                    len(self.pop_dict)
                ))
        stats.end()
        return stats

    def rand_index(self):
        ex = 4 * log(len(self))
        return floor(len(self) * pow(random(), ex))

    def pop(self, index):
        key = self.fitness_indeces[index]
        chrm = self.pop_dict[key].pop(randint(0, len(self.pop_dict[key]) - 1))
        if len(self.pop_dict[key]) == 0:
            del self.pop_dict[key]
        self.fitness_indeces.pop(index)
        return chrm

    def get(self, index):
        key = self.fitness_indeces[index]
        return self.pop_dict[key][randint(0, len(self.pop_dict[key]) - 1)]

    def add(self, chrm):
        if self.pop_dict.get(chrm.fitness) == None:
            self.pop_dict[chrm.fitness] = [chrm]
        else:
            self.pop_dict[chrm.fitness].append(chrm)
        self.fitness_indeces.add(chrm.fitness)

    def __len__(self):
        return len(self.fitness_indeces)

    def __str__(self):
        s = ""
        for k, v in self.pop_dict.items():
            for n in list(v):
                s += str(n) + '\n'
        return s
