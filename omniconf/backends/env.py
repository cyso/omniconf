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
from omniconf.backends.generic import ConfigBackend
from omniconf.keys import join_key
import os


class EnvBackend(ConfigBackend):
    """
    Uses the current process Environment, and allows values in it to
    be retrieved using dotted keys with a specific prefix. By default no
    prefix is assumed.
    """

    def __init__(self, conf=None, prefix=None):
        super(EnvBackend, self).__init__()
        self.prefix = prefix if prefix else ""

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        return EnvBackend(prefix=conf.get(join_key(autoconfigure_prefix,
                                                   "prefix")))

    def get_value(self, setting):
        """
        Retrieves the value for the given :class:`.Setting`. Keys are converted
        as follows:

        * Dots are replaced by underscores
        * The key is uppercased.
        * A prefix is attached to the key

        This means that a key like section.value will be queried like
        ``PREFIX_SECTION_VALUE``. When no prefix is specified,
        ``SECTION_VALUE`` is queried instead.
        """
        _key = setting.key.replace(".", "_").upper()
        if self.prefix:
            _key = "{0}_{1}".format(self.prefix, _key)
        return os.environ[_key]
