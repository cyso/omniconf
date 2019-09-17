# Copyright (c) 2019 Cyso < development [at] cyso . com >
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

import collections

try:
    string_types = (str, unicode)
except NameError:  # pragma: nocover
    string_types = (str, bytes)


class SeparatorSequence(collections.Sequence):
    """
    Splits the given string using the given separator, and provides a
    the result with a read-only Sequence interface.
    """
    def __init__(self, string, separator):
        self.lst = string.split(separator)

    def __getitem__(self, key):
        return self.lst.__getitem__(key)

    def __len__(self):
        return self.lst.__len__()

    def __str__(self):
        return self.lst.__str__()

    __unicode__ = __str__

    def __repr__(self):
        return self.lst.__repr__()


def separator_sequence(separator):
    """
    Returns a function that parses a string value, separates it into parts and
    stores it as a read-only sequence:

    .. code-block:: python

        parser = separator_sequence(",")
        print parser("a,b,c")
        # ['a', 'b', 'c']

    If the input value is already a sequence (but not a string), the value is
    returned as is. The sequence is an instance of :class:`.SeparatorSequence`,
    and can be used as one would normally use a (read-only) tuple or list.
    """
    def factory(value):
        if isinstance(value, collections.Sequence) and \
                not isinstance(value, string_types):
            return value
        return SeparatorSequence(value, separator)
    return factory


def enum(values):
    """
    Returns the original value if it is present in values, otherwise raises a
    RuntimeError.

    .. code-block:: python

        enum_func = enum(["foo", "bar"])
        print enum_func("foo")
        # "foo"
        print enum_func("baz")
        # ...
        # RuntimeError: Invalid value specified, must be one of: foo, bar

    """
    def factory(value):
        if value not in values:
            raise RuntimeError("Invalid value specified, must be one of: {}"
                               .format(", ".join(values)))
        return value
    return factory
