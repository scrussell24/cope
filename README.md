# COntinuous Population Evolution (COPE)

COPE is an evolutionary algorithm much like a genetic algorithm. But unlike a classic
genetic algorhtim, COPE does not generate a new generation from the last. It continuously
generates new indivduals from the Population and inserts them back into the Population. 
This allows the genetic operators and evaluators to be applied to new
individuals completely in parallel, and thus we can speed up the algorithm by adding
more worker process to the pool.

## Diagram

![Cope Diagram](/docs/cope.jpg)

### Population

The Population is the data structure that holds all the individuals
of our population. It is implemented using a sortedList for fast
selection and insertion.

### Manager

The Manager is a separate process with selects two individuals and places them
in the delivery queue. It will then check if the nursery queue has individuals
waiting to be inserted into the population.

### Worker Pool

Workers in the worker pool do all their work in parallel and so we can spin up
many workers to increase the speed of the algorithm. They take a pair of individuals
from the devlivery queue, apply genetic operators like crossover and mutation, to produce
a new individual. This new individual has it's fitness evaluated so the manager
can insert it back into the population in the correct position.

## Setup

create a virtualenv using your preferred method

```
virtualenv -p python3 env
source env/bin/activate
```

install requirements

```
pip install -r requirements-dev.txt
```

## Test

run the unit tests

```
./scripts/unit-test.sh
```

## Examples

There are a couple example files for doing simple list genetic algorithms or gp etc.

```
python list_ga.py
python tree_ga.py
python gp.py
```