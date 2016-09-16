#!/usr/bin/env python
#
# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
import linecache

DESCRIPTION = linecache.getline("README.md", 4)
NAME = "omniconf"
VERSION = "0.1"
BUILD = "AAAAAA"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    license="LGPL3",
    author="Nick Douma",
    author_email="n.douma@nekoconeko.nl",
    url="https://github.com/Cyso/omniconf",
    packages=find_packages(),
    data_files=[],
    install_requires=[],
    setup_requires=[
        "coverage",
        "nose",
        "mock",
        "Sphinx"
    ],
    extras_require={
        "configobj": [
            "configobj"
        ],
        "yaml": [
            "PyYAML"
        ]
    }
)
