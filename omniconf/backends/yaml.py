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
from omniconf.setting import Setting
import yaml


class YamlBackend(ConfigBackend):
    """
    Uses a YAML string as a backend, and allows values in it to
    be retrieved using dotted keys.
    """
    autodetect_settings = (Setting(key="omniconf.yaml.filename", _type=str,
                                   required=False),)

    def __init__(self, conf):
        super(YamlBackend, self).__init__(yaml.load(conf))

    @classmethod
    def autoconfigure(cls, conf):
        if conf.has("omniconf.yaml.filename"):
            return YamlBackend(conf=conf.get("omniconf.yaml.filename"))
