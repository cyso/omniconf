Usage
=====

Basic usage
-----------

The most basic usage of |project| requires the use of the :func:`setting`, :func:`config` and
:func:`omniconf_load` functions:

.. autofunction :: omniconf.setting
.. autofunction :: omniconf.config
.. autofunction :: omniconf.omniconf_load

Define Settings using :func:`setting`:

.. code-block:: python

   from omniconf import setting
   setting("app.username")
   setting("app.hostname")


After defining the Settings, use :func:`omniconf_load` to load values:

.. code-block:: python

   from omniconf import omniconf_load
   omniconf_load()

Afterwards, you can use :func:`config` to retrieve values.

.. code-block:: python

   >>> from omniconf import config
   >>> print config.get("app.username")
   "user"


By default, all Settings defined using :func:`setting` will be stored as :class:`str`. To use another class, do this:

.. code-block:: python

   from omniconf import setting
   setting("app.firstname", _type=unicode)
   setting("app.load_order", _type=list)

Any class can be used. Special cases are added to support :class:`dict`, :class:`list`, :func:`tuple` and
:class:`bool`, which are processed by :mod:`ast`. The class or function passed to `_type` will be called with the value
to process as its only parameter.

Advanced usage
--------------

By default all Settings and Configs are registered in global Registries. These are defined in their respective modules:

.. autodata:: omniconf.config.DEFAULT_REGISTRY
.. autodata:: omniconf.setting.DEFAULT_REGISTRY

This allows you to easily define Settings. Sometimes you might want to have specific Settings and Configs however. You
can achieve this by specifying your own Registries:

.. code-block:: python

   from omniconf.setting import SettingRegistry
   from omniconf.config import ConfigRegistry
   from omniconf import omniconf_load

   settings = SettingRegistry()
   configs = ConfigRegistry(setting_registry=settings)

   setting("app.username", registry=settings)

   omniconf_load(config_registry=configs)


|project| actually uses this mechanism to build the context needed for autoconfiguring. You can check this out in
:func:`autoconfigure_backends`

.. autofunction :: omniconf.loader.autoconfigure_backends
