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

from __future__ import absolute_import
import os


class EnvBackend(object):
    """
    Uses the current process Environment, and allows values in it to
    be retrieved using dotted keys with a specific prefix. If no prefix is specified,
    "OMNICONF" is assumed.
    """
    def __init__(self, conf=None, prefix="OMNICONF"):
        self.prefix = prefix

    def get_value(self, key):
        """
        Retrieves the value for the given key. Keys are converted as follows:

        * Dots are replaced by underscores
        * The key is uppercased.
        * A prefix is attached to the key

        This means that a key like section.value will be queried like PREFIX_SECTION_VALUE.
        """
        _key = key.replace(".", "_").upper()
        if self.prefix:
            _key = "{0}_{1}".format(self.prefix, _key)
        return os.environ[_key]
