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
from omniconf.keys import join_key
from omniconf.setting import Setting
from configobj import ConfigObj


class ConfigObjBackend(ConfigBackend):
    """
    Uses a ConfigObj file (or :mod:`StringIO` instance) as a backend, and
    allows values in it to be retrieved using dotted keys.

    Dots in the keys denote a section in the ConfigObj document. For instance,
    the key `section.subsection.key` will correspond to this document::

        [section]
        [[subsection]]
        key=value

    """

    def __init__(self, conf):
        super(ConfigObjBackend, self).__init__(ConfigObj(conf).dict())

    @classmethod
    def autodetect_settings(cls, autoconfigure_prefix):
        return (Setting(key=join_key(autoconfigure_prefix, "configobj",
                                     "filename"), _type=str, required=False),)

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        filename_key = join_key(autoconfigure_prefix, "configobj", "filename")
        if conf.has(filename_key):
            return ConfigObjBackend(conf=conf.get(filename_key))
        return None
