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
from omniconf.backends.vault import VaultBackend
from tempfile import NamedTemporaryFile
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


class TestVault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with NamedTemporaryFile() as f:
            f.write(VAULT_CONFIG.encode('utf-8'))
            f.flush()

            cls.root_client = hvac.Client(url="http://localhost:18200")
            cls.manager = ServerManager(config_path=f.name, client=cls.root_client)
            cls.manager.start()

            try:
                cls.manager.initialize()
                cls.manager.unseal()
                cls.root_client.token = cls.manager.root_token
                cls.root_client.set_policy("deny", DENY_POLICY)
                cls.root_client.set_policy("normal", NORMAL_POLICY)
                cls.deny_token = cls.root_client.create_token(id="DENY", policies=["deny"])['auth']['client_token']
                cls.normal_token = cls.root_client.create_token(id="NORMAL", policies=["normal"])['auth']['client_token']
            except:
                cls.manager.stop()
                raise

    @classmethod
    def tearDownClass(cls):
        cls.manager.stop()

    def setUp(self):
        self.assertTrue(self.root_client.is_authenticated)
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
        self.assertEqual(self.vault.get_value("secret.foo.bar"), "baz")

    def test_vault_backend_get_no_node(self):
        with self.assertRaises(KeyError):
            self.vault.get_value("secret.foo.bar")

    def test_vault_backend_get_no_value(self):
        self.write_key("secret/foo", bar="baz")
        with self.assertRaises(KeyError):
            self.vault.get_value("secret.foo.baz")

    def test_vault_backend_get_no_access(self):
        self.write_key("secret/foo", bar="baz")
        with self.assertRaises(KeyError):
            self.vault.client.token = self.deny_token
            self.vault.get_value("secret.foo.bar")

    def test_vault_backend_get_with_prefix(self):
        self.write_key("secret/foo", bar="baz")
        self.vault.prefix = "secret"
        self.assertEqual(self.vault.get_value("foo.bar"), "baz")
