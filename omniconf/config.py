# Copyright (c) 2016 Cyso < development [at] cyso . com >
# All rights reserved.
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

from .exceptions import UnknownSettingError, UnconfiguredSettingError
from .settings import DEFAULT_REGISTRY as SETTINGS_REGISTRY


class ConfigRegistry(object):
    def __init__(self, settings_registry=None):
        global SETTINGS_REGISTRY
        if not settings_registry:
            self.settings = SETTINGS_REGISTRY
        self.registry = {}

    def set(self, key, value):
        if not self.settings.has(key):
            raise UnknownSettingError("Trying to configure unregistered key {0}".format(key))
        setting = self.settings.get(key)
        self.settings[key] = setting.type(value)

    def has(self, key):
        if key in self.registry:
            return True
        elif key in self.settings and self.settings[key].default is not None:
            return True
        return False

    def get(self, key):
        if key in self.registry:
            return self.registry[key]
        elif key in self.settings and self.settings[key].default is not None:
            return self.settings[key].default
        raise UnconfiguredSettingError("No value or default available for {0}".format(key))

    def unset(self, key):
        if key in self.registry:
            del self.registry[key]

DEFAULT_REGISTRY = ConfigRegistry()


def config(key, registry=None):
    global DEFAULT_REGISTRY
    if not registry:
        registry = DEFAULT_REGISTRY

    return registry.get(key)
