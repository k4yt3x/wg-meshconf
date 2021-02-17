#!/usr/bin/env sh
pip3 install --user --U setuptools wheel twine build
python3 -m build -nx .
python3 -m twine upload --repository pypi dist/*
