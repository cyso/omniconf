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

from mock import Mock
import unittest
from omniconf.setting import SettingRegistry, Setting, setting, \
                                DEFAULT_REGISTRY


class TestSettingsRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = SettingRegistry()
        self.setting = Setting(key="foo", _type=str)
        self.registry.add(self.setting)

    def test_setting_registry_key_with_string(self):
        self.assertEqual('foo', self.registry._key('foo'))
        self.assertEqual('section.foo', self.registry._key('section.foo'))
        self.assertEqual('section.subsection.foo',
                         self.registry._key('section.subsection.foo'))

    def test_setting_registry_key_with_object(self):
        obj = Mock()
        obj.key = "foo"
        self.assertEqual('foo', self.registry._key(obj))
        obj.key = "section.foo"
        self.assertEqual('section.foo', self.registry._key(obj))
        obj.key = "section.subsection.foo"
        self.assertEqual('section.subsection.foo', self.registry._key(obj))

    def test_setting_registry_clear(self):
        self.assertEqual(len(self.registry.registry), 1)
        self.registry.clear()
        self.assertEqual(len(self.registry.registry), 0)

    def test_setting_registry_add(self):
        self.assertIn(self.setting, self.registry.registry.values())

    def test_setting_registry_has(self):
        self.assertTrue(self.registry.has("foo"))

    def test_setting_registry_get(self):
        self.assertEqual(self.registry.get("foo"), self.setting)

    def test_setting_registry_keys(self):
        self.assertEqual(self.registry.keys(),
                         list(self.registry.registry.keys()))

    def test_setting_registry_list(self):
        self.assertEqual(self.registry.list(),
                         list(self.registry.registry.values()))

    def test_setting_registry_remove(self):
        self.registry.remove(self.setting)
        self.assertNotIn(self.setting, self.registry.registry.values())


class TestSettingMethod(unittest.TestCase):
    def setUp(self):
        self.registry = SettingRegistry()

    def test_setting_method(self):
        _setting = setting("foo", registry=self.registry)
        self.assertTrue(len(self.registry.registry.values()) == 1)
        self.assertIn(_setting, self.registry.registry.values())

    def test_setting_method_with_default_registry(self):
        _setting = setting("foo")
        self.assertIn(_setting, DEFAULT_REGISTRY.registry.values())
        self.assertNotEqual(id(self.registry), id(DEFAULT_REGISTRY))

        DEFAULT_REGISTRY.remove(_setting)
