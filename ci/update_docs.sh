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
# package the docs
#cd _build/html
#tar czf ~/html.tgz .
#cd ../../..

##no jekyll needed for github for rtd theme 
pushd _build/html
touch .nojekyll
popd

popd
#######
#Commenting for now. 1)causes failues in forks; 2) team member can wrongly commit from elsewhere to 
#drilsdown master gh-pages
#would checkout go wrong after travis checks and then commits to github?
#######
# checkout doc branch
#git checkout gh-pages
#git pull git@github.com:Unidata/drilsdown.git gh-pages --allow-unrelated-histories -Xtheirs

# make sure the checkout was successful
#current_branch=$(git branch | grep \* | cut -d ' ' -f2-)
#if [ $current_branch = "gh-pages" ]; then
#    # clear out old docs
#    git rm -rf .
#    rm -fr docs
#    rm -fr .idea
#
#    tar xzf ~/html.tgz
#    # commit and push new docs
#    git add .
#    git commit -a -m "publish the docs"
#    git push origin gh-pages

#    git checkout master
#    else
#    echo "Did not successfully checkout gh-pages branch."
#    echo "Do you have uncommitted changes on your current branch?"
#fi
