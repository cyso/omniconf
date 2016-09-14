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
from configobj import ConfigObj, Section


class ConfigObjBackend(object):
    """
    Uses a ConfigObj file (or StringIO instance) as a backend, and allows values in it to
    be retrieved using dotted keys.
    """
    def __init__(self, conf):
        self.config = ConfigObj(conf)

    def get_value(self, key):
        """
        Retrieves the value for the given key. Will raise a KeyError if the found value is a
        ConfigObj Section rather than an actual value.
        """
        section = self.config
        for _key in key.split("."):
            section = section[_key]
        if isinstance(section, Section):
            raise KeyError(key)
        return section
