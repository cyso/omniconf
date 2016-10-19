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

import hvac
from hvac.tests.util import ServerManager
from mock import patch, ANY
from nose.plugins.skip import SkipTest
from omniconf.backends import available_backends
from omniconf.backends.vault import VaultBackend
from omniconf.config import ConfigRegistry
from omniconf.exceptions import InvalidBackendConfiguration
from omniconf.setting import SettingRegistry, Setting
from tempfile import NamedTemporaryFile
import nose.tools
import unittest

VAULT_CONFIG = """
backend "inmem" {
}

listener "tcp" {
address = "127.0.0.1:18200"
tls_disable = 1
}

disable_mlock = true
"""

NORMAL_POLICY = """
path "secret/*" {
    capabilities = ["read"]
}
"""

DENY_POLICY = """
path "secret/*" {
    capabilities = ["deny"]
}
"""

NORMAL_TOKEN = {
    "id": "NORMAL",
    "policies": ["normal"]
}

DENY_TOKEN = {
    "id": "DENY",
    "policies": ["deny"]
}


def test_vault_backend_in_available_backends():
    nose.tools.assert_in(VaultBackend, available_backends)


class TestVaultBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with NamedTemporaryFile() as f:
            f.write(VAULT_CONFIG.encode('utf-8'))
            f.flush()

            cls.root_client = hvac.Client(url="http://localhost:18200")
            cls.manager = ServerManager(config_path=f.name,
                                        client=cls.root_client)
            try:
                cls.manager.start()
            except OSError:  # pragma: nocover
                raise SkipTest("vault binary not present in PATH.")

            try:
                cls.manager.initialize()
                cls.manager.unseal()
                cls.root_client.token = cls.manager.root_token
                cls.root_client.set_policy("deny", DENY_POLICY)
                cls.root_client.set_policy("normal", NORMAL_POLICY)
                cls.deny_token = cls.root_client.create_token(
                    id="DENY", policies=["deny"])['auth']['client_token']
                cls.normal_token = cls.root_client.create_token(
                    id="NORMAL", policies=["normal"])['auth']['client_token']
            except:  # pragma: nocover
                cls.manager.stop()
                raise

    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()

    def setUp(self):
        self.vault = VaultBackend(url="http://localhost:18200",
                                  auth="token", credentials=self.normal_token)
        self.keys = []

    def tearDown(self):
        self.clean_keys()

    def write_key(self, key, **kwargs):
        self.root_client.write(key, **kwargs)
        self.keys.append(key)

    def clean_keys(self):
        for key in self.keys:
            self.root_client.delete(key)
        self.keys = []

    def test_vault_backend_get(self):
        self.write_key("secret/foo", bar="baz")
        setting = Setting(key="secret.foo.bar", _type=str)
        self.assertEqual(self.vault.get_value(setting), "baz")

    def test_vault_backend_get_no_node(self):
        with self.assertRaises(KeyError):
            self.vault.get_value(Setting(key="secret.foo.bar", _type=str))

    def test_vault_backend_get_no_value(self):
        self.write_key("secret/foo", bar="baz")
        with self.assertRaises(KeyError):
            self.vault.get_value(Setting(key="secret.foo.baz", _type=str))

    def test_vault_backend_get_no_access(self):
        self.write_key("secret/foo", bar="baz")
        with self.assertRaises(KeyError):
            self.vault.client.token = self.deny_token
            self.vault.get_value(Setting(key="secret.foo.bar", _type=str))

    def test_vault_backend_get_with_prefix(self):
        self.write_key("secret/foo", bar="baz")
        self.vault.prefix = "secret"
        setting = Setting(key="foo.bar", _type=str)
        self.assertEqual(self.vault.get_value(setting), "baz")

    def test_vault_backend_without_prefix_or_basepath(self):
        vault = VaultBackend(url="http://localhost:18200",
                             auth="token", credentials=self.normal_token)
        self.assertEqual(vault.prefix, "")

    def test_vault_backend_with_prefix_no_basepath(self):
        vault = VaultBackend(url="http://localhost:18200",
                             auth="token", credentials=self.normal_token,
                             prefix="foo")
        self.assertEqual(vault.prefix, "foo")

    def test_vault_backend_with_basepath_no_prefix(self):
        vault = VaultBackend(url="http://localhost:18200",
                             auth="token", credentials=self.normal_token,
                             base_path="base")
        self.assertEqual(vault.prefix, "base")

    def test_vault_backend_with_prefix_and_basepath(self):
        vault = VaultBackend(url="http://localhost:18200",
                             auth="token", credentials=self.normal_token,
                             prefix="foo", base_path="base")
        self.assertEqual(vault.prefix, "base")


def _setup_vault_autoconfig(prefix):
    settings = SettingRegistry()
    for setting in VaultBackend.autodetect_settings(prefix):
        settings.add(setting)
    return ConfigRegistry(setting_registry=settings)


def test_vault_backend_autoconfigure_invalid_auth():
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    backend = VaultBackend.autoconfigure(configs, prefix)
    nose.tools.assert_is(backend, None)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_token(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["token"], "Bla")
    backend = VaultBackend.autoconfigure(configs, prefix)
    hvac_mock.assert_called_with(url=ANY, token="Bla")
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_client_cert(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["tls_cert"], "CERT")
    configs.set(VaultBackend._config_keys(prefix)["tls_key"], "KEY")
    backend = VaultBackend.autoconfigure(configs, prefix)

    hvac_mock.assert_called_with(url=ANY, cert=("CERT", "KEY"))
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_userpass(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["username"], "USER")
    configs.set(VaultBackend._config_keys(prefix)["password"], "PASS")
    backend = VaultBackend.autoconfigure(configs, prefix)

    hvac_mock.assert_called_with(url=ANY)
    hvac_mock().auth_userpass.assert_called_with("USER", "PASS")
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_ldap(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["ldap_user"], "USER")
    configs.set(VaultBackend._config_keys(prefix)["ldap_pass"], "PASS")
    backend = VaultBackend.autoconfigure(configs, prefix)

    hvac_mock.assert_called_with(url=ANY)
    hvac_mock().auth_ldap.assert_called_with("USER", "PASS")
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_app_id(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["app_id"], "APPID")
    configs.set(VaultBackend._config_keys(prefix)["user_id"], "USERID")
    backend = VaultBackend.autoconfigure(configs, prefix)

    hvac_mock.assert_called_with(url=ANY)
    hvac_mock().auth_app_id.assert_called_with("APPID", "USERID")
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_approle(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["app_role"], "ROLE")
    configs.set(VaultBackend._config_keys(prefix)["app_secret"], "SECRET")
    backend = VaultBackend.autoconfigure(configs, prefix)

    hvac_mock.assert_called_with(url=ANY)
    hvac_mock().auth_approle.assert_called_with("ROLE", "SECRET")
    nose.tools.assert_is_instance(backend, VaultBackend)


@patch("hvac.Client", autospec=True)
def test_vault_backend_autoconfigure_not_authenticated(hvac_mock):
    prefix = "autoconf"
    configs = _setup_vault_autoconfig(prefix)
    configs.set(VaultBackend._config_keys(prefix)["username"], "USER")
    configs.set(VaultBackend._config_keys(prefix)["password"], "PASS")

    hvac_mock().is_authenticated.return_value = False
    with nose.tools.assert_raises(InvalidBackendConfiguration):
        VaultBackend.autoconfigure(configs, prefix)


def test_vault_backend_invalid_auth_mechanism():
    with nose.tools.assert_raises(InvalidBackendConfiguration):
        VaultBackend()
