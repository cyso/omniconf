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
from omniconf.keys import join_key
from omniconf.setting import SettingRegistry, Setting


def autoconfigure_backends(autoconfigure_prefix=None):
    """
    Determine available backends, based on the current configuration available
    in the environment and command line. Backends can define a
    :class:`.Setting` that is required for proper autodetection.

    The result of this function is a list of backends, that are configured and
    ready to use.
    """
    if autoconfigure_prefix is None:
        autoconfigure_prefix = "omniconf"
    backend_settings = SettingRegistry()
    backend_settings.add(Setting(join_key(autoconfigure_prefix, "prefix"),
                                 _type=str))

    # Expand backend_settings with backend specific settings
    for backend in available_backends:
        _settings = backend.autodetect_settings(autoconfigure_prefix)
        if _settings:
            for _setting in _settings:
                backend_settings.add(_setting)

    # Build config for backend settings
    backend_config = ConfigRegistry(setting_registry=backend_settings)
    backend_config.load([backend() for backend in autodetection_backends])

    # Initialize backends based on detected config
    configured_backends = []
    for backend in available_backends:
        _backend = backend.autoconfigure(backend_config, autoconfigure_prefix)
        if _backend:
            configured_backends.append(_backend)

    return configured_backends


def omniconf_load(config_registry=None, backends=None,
                  autoconfigure_prefix=None):
    """
    Fill the provided :class:`.ConfigRegistry`, by default using all available
    backends (as determined by :func:`autoconfigure_backends`. If no
    :class:`ConfigRegistry` is provided, the default :class:`.ConfigRegistry`
    is used. If unset, autoconfigure_prefix will default to "omniconf".
    """
    if not config_registry:
        config_registry = CONFIG_REGISTRY
    if not backends:
        backends = autoconfigure_backends(autoconfigure_prefix)
    config_registry.load(backends)
