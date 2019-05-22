#!/usr/bin/env bash

echo "Building..."
rm dist/*
python setup.py sdist bdist_wheel
pip install dist/*tar.gz

echo "Done."
