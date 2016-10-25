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

    @classmethod
    def add_argument(cls, parser, argument, setting):
        if setting.type is bool:
            if setting.default is None:
                return parser.add_argument(argument)
            elif setting.default is True:
                return parser.add_argument(argument, action="store_false")
            else:
                return parser.add_argument(argument, action="store_true")
        else:
            return parser.add_argument(argument)

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
        parser = argparse.ArgumentParser(add_help=False)

        # Disable forced output from argparse we don't want to display
        parser.print_usage = suppress_output
        parser._print_message = suppress_output

        ArgparseBackend.add_argument(parser, _arg, setting)

        try:
            args = parser.parse_known_args(args=ARGPARSE_SOURCE)[0]
        except SystemExit:
            raise KeyError("Error parsing value for {0}".format(setting.key))

        if getattr(args, _prop) is None:
            raise KeyError("{0} has no value".format(setting.key))
        return getattr(args, _prop)


class ArgparseUsageInformation(object):
    """
    Formats the settings in :class:`.SettingRegistry`, and formats a typical
    Unix usage message for output to console.

    If no name is specified, the value in `sys.argv[0]` will be used.
    Additionally, a custom header and footer can be specified using the
    `top_message` and `bottom_message` parameters.
    """
    def __init__(self, setting_registry, name=None, top_message=None,
                 bottom_message=None):
        self.registry = setting_registry
        self.name = name if name else sys.argv[0]
        self.top_message = top_message
        self.bottom_message = bottom_message

    def _sortable_key(self, key):
        """
        Prefixes keys without a section with an underscore. This will cause
        options like `verbose` to be mentioned before all other options.
        """
        if "." not in key:
            key = "_." + key
        return key

    def _short_metavar_name(self, prop):
        """
        Creates a shortened metavar based on the name of a property. The passed
        property is first uppercased, and split on underscores. Then the first
        letter of each part is used. An property named "foo_bar_baz" will
        result in a metavar named "FBB".
        """
        prop = prop.upper()
        if "_" in prop:
            parts = prop.split("_")
            prop = "".join([part[0] for part in parts])
        elif len(prop) > 3:
            prop = prop[0:3]
        return prop

    def group_settings(self):
        """
        Orders all registered :class:`.Setting` objects by key, and then groups
        then based on the first part of the key.
        """
        keys = sorted(self.registry.keys(),
                      key=lambda x: self._sortable_key(x))
        groups = OrderedDict()
        for key in keys:
            parts = key.split(".")
            group = parts[0] if len(parts) > 1 else "_"
            if group not in groups:
                groups[group] = []
            groups[group].append(key)
        return keys, groups

    def print_usage(self, out=None):
        """
        Leverages :mod:`argparse` to create human readable usage information.
        """
        keys, groups = self.group_settings()
        usage_argparse = argparse.ArgumentParser(
            description=self.top_message, prog=self.name, add_help=False)

        for group, keys in groups.items():
            if group == "_":
                group_argparse = usage_argparse
            else:
                group_argparse = usage_argparse.add_argument_group(group)

            for key in keys:
                _, _prop, _arg = format_argparse_key(key)
                setting = self.registry.get(key)
                argument = ArgparseBackend.add_argument(
                    parser=group_argparse,
                    argument=_arg,
                    setting=setting
                )
                argument.default = setting.default
                argument.type = setting.type
                argument.metavar = self._short_metavar_name(_prop)
                argument.required = setting.required
                argument.help = setting.help

        usage_argparse.print_help(file=out)

    @classmethod
    def check_flag(cls, flags):
        """
        Convenience method to quickly check if the specified flags were
        provided on the command line.
        """
        flag_argparse = argparse.ArgumentParser(add_help=False)
        flag_argparse.add_argument(*flags, dest="flag",
                                   action="store_true")

        return flag_argparse.parse_known_args(args=ARGPARSE_SOURCE)[0].flag
