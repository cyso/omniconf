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

from omniconf.backends.generic import ConfigBackend
from omniconf.loader import autoconfigure_backends, omniconf_load
from omniconf.setting import Setting
from mock import Mock, PropertyMock, patch
import unittest

autodetection_mock = Mock(autospec=ConfigBackend)
autodetect_settings_mock = PropertyMock(return_value=[Setting("omniconf.foo",
                                        _type=str, required=True)])
type(autodetection_mock).autodetect_settings = autodetect_settings_mock

autoconfigure_mock = Mock(autospec=ConfigBackend)
autoconfigure_mock.autoconfigure.return_value = autoconfigure_mock


class TestLoader(unittest.TestCase):
    def setUp(self):
        autodetection_mock.reset_mock()
        autodetect_settings_mock.reset_mock()
        autoconfigure_mock.reset_mock()

    @patch("omniconf.loader.autodetection_backends", new=[autodetection_mock])
    @patch("omniconf.loader.available_backends", new=[autoconfigure_mock])
    def test_autoconfigure_backends(self):
        configured_backends = autoconfigure_backends()

        autodetect_settings_mock.assert_called_once_with()
        autodetection_mock.assert_called_once_with()
        self.assertEqual(configured_backends, [autoconfigure_mock])

    @patch("omniconf.loader.autodetection_backends", new=[autodetection_mock])
    @patch("omniconf.loader.available_backends", new=[autoconfigure_mock])
    @patch("omniconf.loader.CONFIG_REGISTRY")
    def test_omniconf_load(self, registry_mock):
        omniconf_load()
        registry_mock.load.assert_called_once_with([autoconfigure_mock])
