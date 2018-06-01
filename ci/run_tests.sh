#!/usr/bin/env bash
pushd projects/ipython-IDV
tox -e $(echo py$TRAVIS_PYTHON_VERSION | tr -d .)
popd
