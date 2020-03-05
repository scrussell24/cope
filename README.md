# COntinuous Population Evolution (COPE)

COPE is an evolutionary algorithm much like a genetic algorithm.

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