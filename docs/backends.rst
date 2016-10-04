.. _supported-backends:

Supported backends
==================

The following backends are supported as of version |version|:

.. contents :: :local:

backend interface
-----------------

All backends implement the same interface, which allows for easy addition of new (or external backends).

.. autoclass :: omniconf.backends.generic.ConfigBackend
   :members:


commandline arguments
---------------------

Command line arguments are implemented using :mod:`argparse`. This backend is enabled by default.

.. autoclass :: omniconf.backends.argparse.ArgparseBackend
   :members:


environment variables
---------------------

Environments are read from :any:`os.environ`. This backend is enabled by default.

.. autoclass :: omniconf.backends.env.EnvBackend
   :members:


ConfigObj files
---------------

Files in ConfigObj format are supported. This backend is only enabled if `omniconf.configobj.filename` is specified
during setup.

.. autoclass :: omniconf.backends.configobj.ConfigObjBackend
   :members:


JSON files
----------

Files in JSON format are supported. This backend is only enabled if `omniconf.json.filename` is specified during setup.

.. autoclass :: omniconf.backends.json.JsonBackend
   :members:

YAML files
----------

Files in YAML format are supported. This backend is only enabled if `omniconf.yaml.filename` is specified during setup.

.. autoclass :: omniconf.backends.yaml.YamlBackend
   :members:

Hashicorp Vault
---------------

Hashicorp's Vault is supported by using its API. This backend requires several configuration keys to be defined during
setup, see the documentation below for details.

.. autoclass :: omniconf.backends.vault.VaultBackend
   :members:
