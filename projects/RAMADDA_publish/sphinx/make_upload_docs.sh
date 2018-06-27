make singlehtml
cp -a build/singlehtml/* ../docs/
cd ../
git add -A docs
git add -A sphinx
git commit -m 'update docs'
git push origin master
