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
from omniconf.setting import Setting
import yaml


class YamlBackend(object):
    """
    Uses a YAML string as a backend, and allows values in it to
    be retrieved using dotted keys.
    """
    def __init__(self, conf):
        self.config = yaml.load(conf)

    @classmethod
    def autodetect_settings(cls):
        """
        A configobj filename may be specified.
        """
        return (Setting(key="omniconf.yaml.filename", _type=str, required=False),)

    @classmethod
    def autoconfigure(cls, conf):
        """
        Creates an instance configured based on the passed ConfigRegistry.
        """
        if conf.has("omniconf.yaml.filename"):
            return YamlBackend(conf=conf.get("omniconf.yaml.filename"))
        return None

    def get_value(self, key):
        """
        Retrieves the value for the given key.
        """
        section = self.config
        for _key in key.split("."):
            section = section[_key]
        return section
