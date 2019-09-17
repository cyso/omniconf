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

from omniconf.types import separator_sequence, string_or_false, string_bool, \
    enum
import nose.tools


SEPARATOR_SEQUENCES = [
    ("", ",", [""]),
    ("a", ",", ["a"]),
    ("a,b,c", ",", ["a", "b", "c"]),
    ("foo,bar;baz;", ";", ["foo,bar", "baz", ""]),
    (["foo", "bar"], ",", ["foo", "bar"]),
    ([], ",", [])
]


def _test_separator_sequence(_in, _sep, _out):
    seq = separator_sequence(_sep)(_in)
    nose.tools.assert_sequence_equal(seq, _out)
    nose.tools.assert_equal(seq.__str__(), _out.__str__())


def test_separator_sequence():
    for _in, _sep, _out in SEPARATOR_SEQUENCES:
        yield _test_separator_sequence, _in, _sep, _out


STRING_OR_FALSE = [
    ("foo", "foo"),
    ("bar", "bar"),
    (123, 123),
    ("False", False),
    (None, None)
]


def _test_string_or_false(_in, _out):
    nose.tools.assert_equal(string_or_false(_in), _out)


def test_string_or_false():
    for _in, _out in STRING_OR_FALSE:
        yield _test_string_or_false, _in, _out


STRING_BOOL = [
    (0, False),
    ("", False),
    ([], False),
    ({}, False),
    ("False", False),
    (False, False),
    ("True", True),
    (True, True),
    ("0", "0"),
    (1, 1),
    ("1", "1")
]


def _test_string_bool(_in, _out):
    nose.tools.assert_equal(string_bool(_in), _out)


def test_string_bool():
    for _in, _out in STRING_BOOL:
        yield _test_string_bool, _in, _out


ENUM = enum(["foo", "bar", "baz"])
ENUMS = [
    ("foo", "foo", None),
    ("bar", "bar", None),
    ("baz", "baz", None),
    ("fun", None, RuntimeError)
]


def _test_enum(_in, _out, _exc):
    if _exc:
        with nose.tools.assert_raises(_exc):
            ENUM(_in)
    else:
        nose.tools.assert_equal(ENUM(_in), _out)


def test_enum():
    for _in, _out, _exc in ENUMS:
        yield _test_enum, _in, _out, _exc
