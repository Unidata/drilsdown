#!/usr/bin/env bash

# build the docs

# Verify docs build
pwd

pushd docs

pandoc -v
# install prereq
pip install -r requirements.txt
#
make clean
make html


##no jekyll needed for github for rtd theme 
pushd _build/html
touch .nojekyll
popd

popd

