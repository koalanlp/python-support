#!/bin/bash

rm -r dist/
python setup.py bdist_wheel
cd docs
make clean
make html
cd ..
twine-3 upload dist/koalanlp-*.whl