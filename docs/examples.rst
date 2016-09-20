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


Autoconfigure prefix usage
--------------------------

Prefixes are used during autoconfiguring step to load Settings, while trying to avoid name clashes with user defined
Settings. By default, `omniconf.prefix` will be loaded from the environment and cli arguments, by looking for
``OMNICONF_PREFIX`` and ``--omniconf-prefix`` respectively. In these settings, `omniconf` is the prefix.

To change the used during autoconfiguring, do the following:

.. code-block:: python

   from omniconf import omniconf_load
   omniconf_load(config_registry=configs, autoconfigure_prefix="application")

The above example will set the prefix to `application`, which will cause autoconfiguring to look for
``APPLICATION_PREFIX`` and ``--application-prefix`` instead. Good if you don't want to leak that you're using |project|
to your users.


Backend prefix usage
--------------------

Backends may allow a prefix to be defined. By default, this setting is loaded from the ``omniconf.prefix`` key (see
previous section). If defined, this value is passed to all available backends, and will influence how they will load
Config values.

For instance. if ``omniconf.prefix`` is not set, :class:`.EnvBackend` will load ``some.setting`` from the
``SOME_SETTING`` environment variable. If ``omniconf.prefix`` is set to ``app``, the value is loaded from
``APP_SOME_SETTING`` instead. See the :ref:`supported-backends` section for which Backends allow a prefix to be
configured, and how this changes the loading of values.
