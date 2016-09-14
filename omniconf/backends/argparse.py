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
import argparse


class ArgparseBackend(object):
    """
    Uses the current process arguments, and allows values in it to
    be retrieved using dotted keys with a specific prefix. By default no prefix is assumed.
    """
    def __init__(self, conf=None, prefix=None):
        self.prefix = prefix if prefix else ""

    @classmethod
    def autodetect_settings(cls):
        """
        No specific settings needed, we rely on the global prefix setting.
        """
        return None

    @classmethod
    def autoconfigure(cls, conf):
        """
        Creates an instance configured based on the passed ConfigRegistry.
        """
        return ArgparseBackend(prefix=conf.get("omniconf.prefix"))

    def get_value(self, key):
        """
        Retrieves the value for the given key. Keys are converted as follows:

        * Dots are replaced by dashes (-).
        * The key is lowercased.
        * A prefix is attached to the key, if specified

        This means that a key like section.value will be queried like --prefix-section-value.
        """
        _key = key.replace(".", "-").lower()
        _prop = key.replace(".", "_").lower()
        if self.prefix:
            _key = "{0}-{1}".format(self.prefix, _key)
            _prop = "{0}_{1}".format(self.prefix, _prop)
        _arg = "--{0}".format(_key)

        if not _key:
            raise KeyError("Empty keys are not allowed")
        parser = argparse.ArgumentParser()
        parser.add_argument(_arg)
        args = parser.parse_known_args()[0]
        if getattr(args, _prop) is None:
            raise KeyError("{0} has no value".format(_key))
        return getattr(args, _prop)
