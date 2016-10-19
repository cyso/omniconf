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

from omniconf.backends import available_backends
from omniconf.backends.argparse import ArgparseBackend
from omniconf.setting import Setting
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
    (Setting(key="foo", _type=str), "bar", None),
    (Setting(key="section.bar", _type=str), "baz", None),
    (Setting(key="section.subsection.baz", _type=str), "foo", None),
    (Setting(key="", _type=str), None, KeyError),
    (Setting(key="section", _type=str), None, KeyError),
    (Setting(key="unknown", _type=str), None, KeyError),
]


def test_argparse_backend_in_available_backends():
    nose.tools.assert_in(ArgparseBackend, available_backends)


def test_argparse_backend_autoconfigure():
    prefix = "testconf"
    backend = ArgparseBackend.autoconfigure(
        {"{0}.prefix".format(prefix): "bar"}, prefix)
    nose.tools.assert_is_instance(backend, ArgparseBackend)
    nose.tools.assert_equal(backend.prefix, "bar")


def test_argparse_backend_get_value():
    for setting, value, sideeffect in CONFIGS:
        yield _test_get_value, setting, value, sideeffect, None
        yield _test_get_value, setting, value, sideeffect, 'prefix'


def _test_get_value(setting, value, sideeffect, prefix):
    with patch('omniconf.backends.argparse.ARGPARSE_SOURCE',
               ARGS_FILE if not prefix else PREFIX_ARGS_FILE):
        backend = ArgparseBackend(prefix=prefix)
        if sideeffect:
            with nose.tools.assert_raises(sideeffect):
                backend.get_value(setting)
        else:
            nose.tools.assert_equal(backend.get_value(setting), value)
