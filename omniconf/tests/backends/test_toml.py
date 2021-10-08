# Copyright (c) 2020 Cyso < development [at] cyso . com >
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

from __future__ import unicode_literals
from omniconf.backends import available_backends
try:
    from omniconf.backends.toml import TomlBackend
except ImportError:
    from nose.plugins.skip import SkipTest
    raise SkipTest("toml or tomli library not installed.")
from omniconf.config import ConfigRegistry
from omniconf.setting import SettingRegistry, Setting
from mock import mock_open
try:
    from io import StringIO
except ImportError:  # pragma: nocover
    from StringIO import StringIO
import nose.tools

TOML_FILE = """
foo = "bar"
dotted.keys.are = "supported"

[section]
bar = "baz"

[section.subsection]
baz = "foo"

[bar]
sub = "bar-sub-value"
"""

CONFIGS = [
    ("foo", "bar", None),
    ("dotted.keys.are", "supported", None),
    ("section.bar", "baz", None),
    ("section.subsection.baz", "foo", None),
    ("", None, KeyError),
    ("section", {"bar": "baz", "subsection": {"baz": "foo"}}, None),
    ("unknown", None, KeyError),
    ("bar.sub", "bar-sub-value", None)
]


def test_toml_backend_in_available_backends():
    nose.tools.assert_in(TomlBackend, available_backends)


def test_toml_backend_autoconfigure():
    from omniconf.backends import toml as omniconf_backend_toml
    omniconf_backend_toml.open = mock_open(read_data=TOML_FILE)
    prefix = "testconf"
    settings = SettingRegistry()
    settings.add(TomlBackend.autodetect_settings(prefix)[0])
    conf = ConfigRegistry(setting_registry=settings)

    backend = TomlBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is(backend, None)

    conf.set("{0}.toml.filename".format(prefix), "bar")
    backend = TomlBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is_instance(backend, TomlBackend)


def test_toml_backend_get_value():
    for key, value, sideeffect in CONFIGS:
        yield _test_get_value, key, value, sideeffect


def _test_get_value(key, value, sideeffect):
    f = StringIO(TOML_FILE)
    backend = TomlBackend(f)
    setting = Setting(key=key, _type=str)
    if sideeffect:
        with nose.tools.assert_raises(sideeffect):
            backend.get_value(setting)
    else:
        nose.tools.assert_equal(backend.get_value(setting), value)
