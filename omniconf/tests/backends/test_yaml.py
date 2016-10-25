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

from omniconf.backends import available_backends
from omniconf.backends.yaml import YamlBackend
from omniconf.config import ConfigRegistry
from omniconf.setting import SettingRegistry, Setting
from mock import patch, mock_open
import nose.tools

YAML_FILE = """
---
foo: bar
section:
  bar: baz
  subsection:
    baz: foo
---
bar:
  sub: bar-sub-value
"""

CONFIGS = [
    ("foo", "bar", None),
    ("section.bar", "baz", None),
    ("section.subsection.baz", "foo", None),
    ("", None, KeyError),
    ("section", {"bar": "baz", "subsection": {"baz": "foo"}}, None),
    ("unknown", None, KeyError),
    ("bar.sub", "bar-sub-value", None)
]


def test_yaml_backend_in_available_backends():
    nose.tools.assert_in(YamlBackend, available_backends)


@patch("yaml.load")
def test_yaml_backend_autoconfigure(mock):
    from omniconf.backends import yaml as omniconf_backend_yaml
    omniconf_backend_yaml.open = mock_open(read_data=YAML_FILE)
    prefix = "testconf"
    settings = SettingRegistry()
    settings.add(YamlBackend.autodetect_settings(prefix)[0])
    conf = ConfigRegistry(setting_registry=settings)

    backend = YamlBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is(backend, None)

    conf.set("{0}.yaml.filename".format(prefix), "bar")
    backend = YamlBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is_instance(backend, YamlBackend)


def test_yaml_backend_get_value():
    for key, value, sideeffect in CONFIGS:
        yield _test_get_value, key, value, sideeffect


def _test_get_value(key, value, sideeffect):
    backend = YamlBackend(YAML_FILE)
    setting = Setting(key=key, _type=str)
    if sideeffect:
        with nose.tools.assert_raises(sideeffect):
            backend.get_value(setting)
    else:
        nose.tools.assert_equal(backend.get_value(setting), value)
