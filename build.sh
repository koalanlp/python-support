#!/bin/bash

pip3 install --upgrade sphinx sphinx_rtd_theme twine pytest pypandoc

rm -r dist/
python3 setup.py bdist_wheel
mv docs/.nojekyll ./
mv docs/index.html ./
make clean
make html
mv ./.nojekyll docs/
mv ./index.html docs/
twine upload dist/koalanlp-*.whl

VERSION=`ls dist | grep koalanlp | cut -d- -f2`
git add docs/
git add -i
git commit -m "Release: v${VERSION}"
git tag v${VERSION}
git push --all