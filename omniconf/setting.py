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


class SettingRegistry(object):
    """
    A registry of defined :class:`Setting` objects.
    """
    def __init__(self):
        self.registry = {}

    def _key(self, setting):
        if isinstance(setting, str):
            return setting
        else:
            return setting.key

    def clear(self):
        self.registry = {}

    def add(self, setting):
        """
        Register a Setting.
        """
        self.registry[setting.key] = setting
        return setting

    def has(self, key):
        """
        Check if a Setting has been registered under the specified key.
        """
        return key in self.registry

    def get(self, key):
        """
        Retrieves the Setting for the given key.
        """
        return self.registry[key]

    def keys(self):
        """
        Returns the registered keys.
        """
        return list(self.registry.keys())

    def list(self):
        """
        Returns the configured Settings as a list.
        """
        return list(self.registry.values())

    def remove(self, setting):
        """
        Removes the Setting with the given key.
        """
        del self.registry[self._key(setting)]

DEFAULT_REGISTRY = SettingRegistry()
"""
Global :class:`.SettingRegistry` which will be used when no specific
:class:`.SettingRegistry` is defined.
"""


class Setting(object):
    """
    A :class:`.Setting` is registered under a specific key and with a specific
    type (:class:`str`, :class:`dict`, :class:`list`, etc). A default may also
    be specified, which allows a config to be returned without a value being
    specifically defined (also see :class:`.ConfigRegistry`). A
    :class:`.Setting` may be marked as required, which will cause an exception
    to be thrown when no value is found when autoconfiguring. A help message
    may be specified for documentation purposes.
    """
    def __init__(self, key, _type, required=False, default=None, help=None):
        self.key = key
        self.type = _type
        self.required = required
        self.default = default
        self.help = help


def setting(key, _type=str, required=False, default=None, help=None,
            registry=None):
    """
    Register a new :class:`.Setting` with the given key.
    """
    if not registry:
        registry = DEFAULT_REGISTRY

    return registry.add(Setting(key, _type, required, default, help))
