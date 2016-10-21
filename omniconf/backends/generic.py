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


class ConfigBackend(object):
    """
    Defines a configuration backend, which provides configuration values
    based on keys.
    """

    def __init__(self, conf=None):
        self.config = conf

    @classmethod
    def autodetect_settings(cls, autoconfigure_prefix):
        """
        Returns a tuple of :class:`.Setting` objects, that are required for
        :func:`autoconfigure` to complete successfully.
        """
        return ()

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        """
        Called with a :class:`.ConfigRegistry`, the result of this method must
        be either a new instance of this class, or :any:`None`. This method
        is automatically called during the autoconfigure phase.
        """
        raise NotImplementedError("This method must be implemented")

    def get_value(self, setting):
        """
        Retrieves the value for the given :class:`.Setting`.
        """
        section = self.config
        for _key in setting.key.split("."):
            section = section[_key]
        return section
