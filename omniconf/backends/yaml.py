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

    def __init__(self, conf):
        super(YamlBackend, self).__init__(yaml.load(conf))

    @classmethod
    def autodetect_settings(cls, autoconfigure_prefix):
        return (Setting(key="{0}.yaml.filename".format(autoconfigure_prefix),
                        _type=str, required=False),)

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        if conf.has("{0}.yaml.filename".format(autoconfigure_prefix)):
            return YamlBackend(conf=conf.get("{0}.yaml.filename"
                                             .format(autoconfigure_prefix)))
