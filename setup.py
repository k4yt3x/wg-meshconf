#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: wg-meshconf PyPI setup file
Creator: dimon222
Date Created: January 11, 2021
Last Modified: January 11, 2021

Dev: K4YT3X
Last Modified: January 12, 2021
"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="wg-meshconf",
    version="2.1.1",
    author="K4YT3X",
    author_email="k4yt3x@k4yt3x.com",
    description="wg-meshconf is a tool that will help you to generate peer configuration files for WireGuard mesh networks",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/k4yt3x/wg-meshconf",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    install_requires=["prettytable"],
    classifiers=[
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["wg-meshconf = wg_meshconf:main"]},
)
