#!/bin/bash
python -m pycodestyle --max-line-length=110 cope/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Lint Error"
    exit $retVal
fi

python -m mypy --ignore-missing-imports cope/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Type Checking Error"
    exit $retVal
fi

python -m pytest --cov=cope/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Test Error"
    exit $retVal
fi