#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: wg-meshconf PyPI setup file
Creator: dimon222
Date Created: January 11, 2021
Last Modified: January 11, 2021

Dev: K4YT3X
Last Modified: May 22, 2021

pip3 install --user -U setuptools wheel twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository pypi dist/*
"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="wg-meshconf",
    version="2.3.0",
    author="K4YT3X",
    author_email="k4yt3x@k4yt3x.com",
    description="wg-meshconf is a tool that will help you to generate peer configuration files for WireGuard mesh networks",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/k4yt3x/wg-meshconf",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    install_requires=["cryptography", "prettytable"],
    classifiers=[
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["wg-meshconf = wg_meshconf:main"]},
)
