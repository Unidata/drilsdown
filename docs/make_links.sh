#!/bin/bash
rm -rf ./examples
#ln -s ../UseCase_Examples examples currently links have a problem 
#https://github.com/spatialaudio/nbsphinx/issues/49
mkdir examples
cp -rf ../UseCase_Examples/* examples/
