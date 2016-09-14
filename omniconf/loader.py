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

from omniconf.backends import available_backends, autodetection_backends
from omniconf.config import ConfigRegistry, DEFAULT_REGISTRY as CONFIG_REGISTRY
from omniconf.setting import SettingRegistry, Setting, DEFAULT_REGISTRY as SETTING_REGISTRY


def autoconfigure_backends():
    backend_settings = SettingRegistry()
    backend_settings.add(Setting("omniconf.prefix", _type=str))

    # Expand backend_settings with backend specific settings
    for backend in available_backends:
        _settings = backend.autodetect_settings
        if _settings:
            for _setting in _settings:
                backend_settings.add(_setting)

    # Build config for backend settings
    backend_config = ConfigRegistry(setting_registry=backend_settings)
    backend_config.load([backend() for backend in autodetection_backends])

    # Initialize backends based on detected config
    configured_backends = []
    for backend in available_backends:
        _backend = backend.autoconfigure(backend_config)
        if _backend:
            configured_backends.append(_backend)

    return configured_backends


def omniconf_load(setting_registry=None, config_registry=None, autodetect=True, backends=None):
    if not setting_registry:
        setting_registry = SETTING_REGISTRY
    if not config_registry:
        config_registry = CONFIG_REGISTRY
    if not backends:
        backends = []

    configured_backends = autoconfigure_backends()
    config_registry.load(configured_backends)
