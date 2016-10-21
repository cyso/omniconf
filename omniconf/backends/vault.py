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
from omniconf.exceptions import InvalidBackendConfiguration
from omniconf.keys import join_key, join_key_parts
from omniconf.setting import Setting
import hvac


class VaultBackend(ConfigBackend):
    """
    Uses Hashicorp's Vault as a backend, and allows values in it to be
    retrieved using dotted keys.

    **Key translation**

    Dotted keys are translated into an URL path, which is then optionally
    prepended by the configured backend prefix. The last part of the path is
    used as a property to retrieve. If a base_path is also configured, it
    overrides the backend prefix.

    For instance, a setting with key `setting.foo.bar` will be translated into
    path ``setting/foo``, from which the property with key ``bar`` will be
    retrieved. Because Vault nodes are grouped by backend, it usually makes
    sense to define `base_path` as `secret`, which corresponds to the Generic
    backend of Vault. In this example, the example key will be translated into
    path ``secret/setting/foo``, from which the property with key `bar` will be
    retrieved.

    **API Connection**

    The URL endpoint which |project| will default to ``http://localhost:8200``,
    and can be configured using the configuration key ``omniconf.vault.url``,
    assuming the ``autoconfigure_prefix`` is set to `omniconf`.

    **Authentication**

    Vault's API requires some form of authentication, of which the following
    are supported:

        * `Tokens <https://www.vaultproject.io/docs/auth/token.html>`_
        * `TLS certificates <https://www.vaultproject.io/docs/auth/cert.html>`_
        * `Username & Password \
           <https://www.vaultproject.io/docs/auth/userpass.html>`_
        * `LDAP <https://www.vaultproject.io/docs/auth/ldap.html>`_
        * `App ID <https://www.vaultproject.io/docs/auth/app-id.html>`_
        * `AppRole <https://www.vaultproject.io/docs/auth/approle.html>`_

    Retrieval of Vault data requires an ACL to be defined, which goes beyond
    the scope of this documentation. |project| only needs read rights on the
    keys it tries to access.

    Selection of what authentication method is used depends on which
    configuration is present during setup. For all the following examples, the
    ``autoconfigure_prefix`` is assumed to be `omniconf`:

        * Token authentication is used if ``omniconf.vault.auth.token``
          is defined.
        * TLS certificates authentication is used if both
          ``omniconf.vault.auth.tls.cert.filename`` and
          ``omniconf.vault.auth.tls.key.filename`` are defined.
        * Username and Password authentication is used if both
          ``omniconf.vault.auth.userpass.username`` and
          ``omniconf.vault.auth.userpass.password`` are defined.
        * LDAP authentication is used if both
          ``omniconf.vault.auth.ldap.username`` and
          ``omniconf.vault.auth.ldap.password`` are defined.
        * App ID authentication is used if both
          ``omniconf.vault.auth.appid.app_id`` and
          ``omniconf.vault.auth.appid.user_id`` are defined.
        * AppRole authentication is used if both
          ``omniconf.vault.auth.approle.role_id`` and
          ``omniconf.vault.auth.approle.secret_id`` are defined.

    The above order is also the order in which the configuration values are
    looked up. The first one to satisfy the conditions is used, and no further
    attepts are made if configuration fails.
    """

    def __init__(self, conf=None, prefix=None, url=None, auth=None,
                 credentials=None, base_path=None):
        if not prefix:
            prefix = ""
        if base_path:
            prefix = base_path
        self.prefix = prefix

        if auth == "token":
            self.client = hvac.Client(url=url, token=credentials)

        elif auth == "client_cert":
            self.client = hvac.Client(url=url, cert=credentials)
            self.client.auth_tls()

        elif auth in ("userpass", "ldap", "appid", "approle"):
            identifier, secret = credentials
            self.client = hvac.Client(url=url)
            if auth == "userpass":
                self.client.auth_userpass(identifier, secret)
            elif auth == "ldap":
                self.client.auth_ldap(identifier, secret)
            elif auth == "appid":
                self.client.auth_app_id(identifier, secret)
            else:
                self.client.auth_approle(identifier, secret)

        else:
            raise InvalidBackendConfiguration(
                "Invalid authentication mechanism selected for Vault backend.")

        if not self.client.is_authenticated():
            raise InvalidBackendConfiguration(
                "Vault backend is not authenticated")

    @classmethod
    def _config_keys(cls, autoconfigure_prefix):
        return {
            "url": join_key(autoconfigure_prefix, "vault", "url"),
            "base_path": join_key(autoconfigure_prefix, "vault", "base_path"),
            "token": join_key(autoconfigure_prefix, "vault", "auth", "token"),
            "tls_cert": join_key(autoconfigure_prefix, "vault", "auth", "tls",
                                 "cert", "filename"),
            "tls_key": join_key(autoconfigure_prefix, "vault", "auth", "tls",
                                "key", "filename"),
            "username": join_key(autoconfigure_prefix, "vault", "auth",
                                 "userpass", "username"),
            "password": join_key(autoconfigure_prefix, "vault", "auth",
                                 "userpass", "password"),
            "ldap_user": join_key(autoconfigure_prefix, "vault", "auth",
                                  "ldap", "username"),
            "ldap_pass": join_key(autoconfigure_prefix, "vault", "auth",
                                  "ldap", "password"),
            "app_id": join_key(autoconfigure_prefix, "vault", "auth", "appid",
                               "app_id"),
            "user_id": join_key(autoconfigure_prefix, "vault", "auth", "appid",
                                "user_id"),
            "app_role": join_key(autoconfigure_prefix, "vault", "auth",
                                 "approle", "role_id"),
            "app_secret": join_key(autoconfigure_prefix, "vault", "auth",
                                   "approle", "secret_id")
        }

    @classmethod
    def autodetect_settings(cls, autoconfigure_prefix):
        settings = []
        for name, key in cls._config_keys(autoconfigure_prefix).items():
            if name == "url":
                settings.append(Setting(key=key, _type=str, required=False,
                                        default="http://localhost:8200"))
            else:
                settings.append(Setting(key=key, _type=str, required=False))
        return settings

    @classmethod
    def autoconfigure(cls, conf, autoconfigure_prefix):
        keys = cls._config_keys(autoconfigure_prefix)
        url = conf.get(keys['url'])

        if conf.has(keys['token']):
            return VaultBackend(url=url, auth="token",
                                credentials=conf.get(keys['token']))

        elif conf.has(keys['tls_cert']) and conf.has(keys['tls_key']):
            return VaultBackend(url=url, auth="client_cert",
                                credentials=(conf.get(keys['tls_cert']),
                                             conf.get(keys['tls_key'])))

        elif conf.has(keys['username']) and conf.has(keys['password']):
            return VaultBackend(url=url, auth="userpass",
                                credentials=(conf.get(keys['username']),
                                             conf.get(keys['password'])))

        elif conf.has(keys['ldap_user']) and conf.has(keys['ldap_pass']):
            return VaultBackend(url=url, auth="ldap",
                                credentials=(conf.get(keys['ldap_user']),
                                             conf.get(keys['ldap_pass'])))

        elif conf.has(keys['app_id']) and conf.has(keys['user_id']):
            return VaultBackend(url=url, auth="appid",
                                credentials=(conf.get(keys['app_id']),
                                             conf.get(keys['user_id'])))

        elif conf.has(keys['app_role']) and conf.has(keys['app_secret']):
            return VaultBackend(url=url, auth="approle",
                                credentials=(conf.get(keys['app_role']),
                                             conf.get(keys['app_secret'])))

        return None

    def get_value(self, setting):
        parts = setting.key.split(".")
        if self.prefix:
            parts.insert(0, self.prefix)

        data_key = parts.pop()
        path = join_key_parts("/", parts)

        try:
            node = self.client.read(path)
        except hvac.exceptions.Forbidden:
            raise KeyError("No access to Vault data node at {0}".format(path))
        if not node:
            raise KeyError("No Vault data node at {0}".format(path))
        return node['data'][data_key]
