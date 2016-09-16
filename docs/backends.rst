.. _supported-backends:

Supported backends
==================

The following backends are supported as of version |version|:

* commandline arguments (using argparse)
* environment variables
* ConfigObj files
* JSON files
* YAML files (using PyYAML)

backend interface
-----------------

All backends implement the same interface, which allows for easy addition of new (or external backends).

.. autoclass :: omniconf.backends.generic.ConfigBackend
   :members:


commandline arguments
---------------------

Command line arguments are implemented using argparse. This backend is enabled by default.

.. autoclass :: omniconf.backends.argparse.ArgparseBackend
   :members:


environment variables
---------------------

Environments are read from os.environ. This backend is enabled by default.

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
