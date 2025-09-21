#!/bin/bash

# Formatter
black .

# Linter
pylint .

# Dependencies Sort
isort . --profile=black

# Run unit tests
python -m coverage run -m pytest  -v -s