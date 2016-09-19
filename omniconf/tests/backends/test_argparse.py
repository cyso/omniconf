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

from omniconf.backends.argparse import ArgparseBackend
from mock import patch
import nose.tools

ARGS_FILE = [
    "script.py",
    "--foo", "bar",
    "--section-bar", "baz",
    "--section-subsection-baz", "foo"
]

PREFIX_ARGS_FILE = [
    "script.py",
    "--prefix-foo", "bar",
    "--prefix-section-bar", "baz",
    "--prefix-section-subsection-baz", "foo"
]

CONFIGS = [
    ("foo", "bar", None),
    ("section.bar", "baz", None),
    ("section.subsection.baz", "foo", None),
    ("", None, KeyError),
    ("section", None, KeyError),
    ("unknown", None, KeyError)
]


def test_argparse_backend_autoconfigure():
    backend = ArgparseBackend.autoconfigure({"omniconf.prefix": "bar"})
    nose.tools.assert_is_instance(backend, ArgparseBackend)
    nose.tools.assert_equal(backend.prefix, "bar")


def test_argparse_backend_get_value():
    for key, value, sideeffect in CONFIGS:
        yield _test_get_value, key, value, sideeffect, None
        yield _test_get_value, key, value, sideeffect, 'prefix'


def _test_get_value(key, value, sideeffect, prefix):
    with patch('omniconf.backends.argparse.ARGPARSE_SOURCE', ARGS_FILE if not prefix else PREFIX_ARGS_FILE):
        backend = ArgparseBackend(prefix=prefix)
        if sideeffect:
            with nose.tools.assert_raises(sideeffect):
                backend.get_value(key)
        else:
            nose.tools.assert_equal(backend.get_value(key), value)
