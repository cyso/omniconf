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

from omniconf.exceptions import UnknownSettingError, UnconfiguredSettingError
from omniconf.setting import DEFAULT_REGISTRY as SETTING_REGISTRY
import ast


def unrepr(s, _type):
    if isinstance(s, _type):
        return s
    if not s:
        return s
    return ast.literal_eval(s)


class ConfigRegistry(object):
    """
    A registry of Configured values for a :class:`.SettingRegistry`.
    """
    def __init__(self, setting_registry=None):
        if not setting_registry:
            self.settings = SETTING_REGISTRY
        else:
            self.settings = setting_registry
        self.clear()

    def clear(self):
        self.registry = {}

    def set(self, key, value):
        """
        Configures the value for the given key. The value will be converted to
        the type defined in the :class:`.Setting`, by calling the type as a
        function with the value as the only argument. Trying to configure a
        value under an unknown key will result in an UnknownSettingError.
        """
        if not self.settings.has(key):
            raise UnknownSettingError("Trying to configure unregistered key "
                                      "{0}".format(key))
        setting = self.settings.get(key)

        if setting.type in (list, dict, tuple, bool):
            self.registry[key] = unrepr(value, setting.type)
        else:
            self.registry[key] = setting.type(value)

    def has(self, key):
        """
        Checks if a value has been configured for the given key, or if a
        default value is present.
        """
        if key in self.registry:
            return True
        elif self.settings.has(key) and \
                self.settings.get(key).default is not None:
            return True
        return False

    def get(self, key):
        """
        Returns the configured value for the given key, or the default value if
        the key was not configured.
        """
        if key in self.registry:
            return self.registry[key]
        elif self.settings.has(key) and \
                self.settings.get(key).default is not None:
            return self.settings.get(key).default
        elif self.settings.has(key) and not self.settings.get(key).required:
            return None
        raise UnconfiguredSettingError("No value or default available for {0}"
                                       .format(key))

    def list(self):
        """
        Returns all configured values as a dict.
        """
        return self.registry

    def unset(self, key):
        """
        Removes the value for a given key from the registry.
        """
        if key in self.registry:
            del self.registry[key]

    def load(self, backends):
        """
        Attempt to configure all settings defined in the
        :class:`.SettingRegistry` using the provided backends. If a setting
        was attempting to load, and no value found and no default was set, an
        UnconfiguredSettingError is raised.
        """
        for setting in self.settings.list():
            if setting.key in self.registry:
                continue
            for backend in backends:
                try:
                    self.set(setting.key, backend.get_value(setting))
                except KeyError:
                    pass
                except ValueError as ve:
                    raise ValueError("An invalid value was specified for "
                                     "{0}: {1}".format(setting.key, str(ve)))

            if not self.has(setting.key) and setting.required:
                raise UnconfiguredSettingError("No value was configured for "
                                               "{0}".format(setting.key))

DEFAULT_REGISTRY = ConfigRegistry()
"""
Global :class:`.ConfigRegistry` which will be used when no specific
:class:`.ConfigRegistry` is defined.
"""


def config(key, registry=None):
    """
    Retrieves the configured value for a given key. If no specific registry is
    specified, the value will be retrieved from the default
    :class:`.ConfigRegistry`.
    """
    if not registry:
        registry = DEFAULT_REGISTRY

    return registry.get(key)
