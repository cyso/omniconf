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
from collections import OrderedDict
from omniconf.backends.generic import ConfigBackend
from omniconf.keys import join_key
import argparse
import sys

ARGPARSE_SOURCE = sys.argv[1:]


def suppress_output(*args, **kwargs):  # pragma: nocover
    pass


def format_argparse_key(key, prefix=None):
    _key = key.replace(".", "-").lower()
    _prop = key.replace(".", "_").lower()
    if prefix:
        _key = "{0}-{1}".format(prefix, _key)
        _prop = "{0}_{1}".format(prefix, _prop)
    _arg = "--{0}".format(_key)

    return _key, _prop, _arg


class ArgparseBackend(ConfigBackend):
    """
    Uses the current process arguments, and allows values in it to
    be retrieved using dotted keys with a specific prefix. By default no
    prefix is assumed.
    """

    def __init__(self, conf=None, prefix=None):
        super(ArgparseBackend, self).__init__()
        self.prefix = prefix if prefix else ""

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        return ArgparseBackend(prefix=conf.get(join_key(autoconfigure_prefix,
                                                        "prefix")))

    def get_value(self, setting):
        """
        Retrieves the value for the given :class:`.Setting`. Keys are
        converted as follows:

        * Dots are replaced by dashes (-).
        * The key is lowercased.
        * A prefix is attached to the key, if specified

        This means that a key like section.value will be queried like
        ``--prefix-section-value``. When no prefix is specified,
        ``--section-value`` is queried instead.

        Special handling is added for boolean Settings with a default
        specified, which works as follows:

        * Settings with `_type=bool` and no default will be processed
          as normal.
        * Settings with `_type=bool`, and where the default value is True will
          be specified as an argparse argument with `action=store_false`.
        * Settings with `_type=bool`, and where the default value is False will
          be specified as an argparse argument with `action=store_true`.
        """
        _key, _prop, _arg = format_argparse_key(setting.key, self.prefix)

        if not _key:
            raise KeyError("Empty keys are not allowed")
        parser = argparse.ArgumentParser()

        # Disable forced output from argparse we don't want to display
        parser.print_usage = suppress_output
        parser._print_message = suppress_output

        if setting.type is bool:
            if setting.default is None:
                parser.add_argument(_arg)
            elif setting.default is True:
                parser.add_argument(_arg, action="store_false")
            else:
                parser.add_argument(_arg, action="store_true")
        else:
            parser.add_argument(_arg)

        try:
            args = parser.parse_known_args(args=ARGPARSE_SOURCE)[0]
        except SystemExit:
            raise KeyError("Error parsing value for {0}".format(setting.key))

        if getattr(args, _prop) is None:
            raise KeyError("{0} has no value".format(setting.key))
        return getattr(args, _prop)


class ArgparseUsageInformation(object):
    def __init__(self, setting_registry, name=None, top_message=None,
                 bottom_message=None):
        self.registry = setting_registry
        self.name = name if name else sys.argv[0]
        self.top_message = top_message
        self.bottom_message = bottom_message

    def _sortable_key(self, key):
        if "." not in key:
            key = "_." + key
        return key

    def group_settings(self):
        keys = sorted(self.registry.keys(), key=lambda x: self._sortable_key(x))
        groups = OrderedDict()
        for key in keys:
            parts = key.split(".")
            group = parts[0] if len(parts) > 1 else "_"
            if not group in groups:
                groups[group] = []
            groups[group].append(key)
        return keys, groups

    def print_usage(self, out=None):
        keys, groups = self.group_settings()
        help_argparse = argparse.ArgumentParser(
            description=self.top_message, prog=self.name, add_help=False)

        for group, keys in groups.items():
            if group == "_":
                group_argparse = help_argparse
            else:
                group_argparse = help_argparse.add_argument_group(group)

            for key in keys:
                _, _, _arg = format_argparse_key(key)
                setting = self.registry.get(key)
                group_argparse.add_argument(
                    _arg,
                    default=setting.default,
                    type=setting.type,
                    required=setting.required,
                    help=setting.help
                )

        help_argparse.print_help(file=out)
