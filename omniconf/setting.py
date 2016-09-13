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


class SettingsRegistry(object):
    registry = {}

    @classmethod
    def _key(cls, setting):
        if isinstance(setting, str):
            return setting
        else:
            return setting.key

    @classmethod
    def add(cls, setting):
        cls.registry[setting.key] = setting
        return setting

    @classmethod
    def has(cls, key):
        return key in cls.registry

    @classmethod
    def get(cls, key):
        return cls.registry[key]

    @classmethod
    def remove(cls, setting):
        del cls.registry[cls._key(setting)]

DEFAULT_REGISTRY = SettingsRegistry()


class Setting(object):
    def __init__(self, key, _type, default=None, help=None):
        self.key = key
        self.type = _type
        self.default = default
        self.help = help


def setting(key, _type=str, default=None, help=None, registry=None):
    global DEFAULT_REGISTRY
    if not registry:
        registry = DEFAULT_REGISTRY

    return registry.add(Setting(key, _type, default, help))
