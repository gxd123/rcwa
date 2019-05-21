#!/usr/bin/env bash

echo "Building..."
rm dist/*
python setup.py sdist bdist_wheel
pip2 install dist/*tar.gz

echo "Done."
