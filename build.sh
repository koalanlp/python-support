#!/bin/bash

pip install sphinx sphinx_rtd_theme twine pytest

rm -r dist/
python setup.py bdist_wheel
cd docs
make clean
make html
cd ..
twine upload dist/koalanlp-*.whl

VERSION=`ls dist | grep koalanlp | cut -d- -f2`
git add docs/
git add -i
git commit -m "Release: v${VERSION}"
git tag v${VERSION}
git push --all