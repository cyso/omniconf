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

DESCRIPTION = "A Python library that makes configuring your application "\
              "independent from your configuration backend."
LONG_DESCRIPTION = open('README.rst').read()
NAME = "omniconf"
VERSION = "1.1.0"
BUILD = "f7d50ed"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license="LGPL3",
    author="Nick Douma",
    author_email="n.douma@nekoconeko.nl",
    url="https://github.com/cyso/omniconf",
    packages=find_packages(),
    data_files=[('', ['README.rst'])],
    install_requires=[],
    extras_require={
        "configobj": [
            "configobj"
        ],
        "vault": [
            "hvac"
        ],
        "yaml": [
            "PyYAML"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: "
            "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: "
            "Implementation :: CPython",
        "Programming Language :: Python :: "
            "Implementation :: Jython",
        "Programming Language :: Python :: "
            "Implementation :: PyPy",
        "Topic :: Software Development :: "
            "Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities"
    ]
)
