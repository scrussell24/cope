#!/bin/bash
python -m pycodestyle --max-line-length=110 ape/
# looks like linter isn't updated for walrus operator
# retVal=$?
# if [ $retVal -ne 0 ]; then
#     echo "Lint Error"
#     exit $retVal
# fi

python -m mypy --ignore-missing-imports ape/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Type Checking Error"
    exit $retVal
fi

python -m pytest --cov=ape/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Test Error"
    exit $retVal
fi