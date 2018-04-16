#!/usr/bin/env bash
cd projects/ipython-IDV
tox -e $(echo py$TRAVIS_PYTHON_VERSION | tr -d .)