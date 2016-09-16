Design principles
=================

The design of |project| is based around the following principles:

* Defining settings must be easy.
* Configuration of values must be easy.
* Multiple sources for configuration must be allowed and supported.
* Fine-grained configuration should be an option.
* Backends should be easy to implement.

Configuring an application can be hard, and it gets more complex if more than one way to configure must be supported.
|project| aims to separate definition of Settings and the loading of the Config, so that multiple Backends can
be easily used and changed.

Keys
====

All Settings and Configs are defined using a simple key. The key should only contain ASCII characters (altough this
is not validated). The following are valid keys::

   username
   password
   application.module.setting

Dots denote a section, and are mainly used to group similar keys. They can also be used by backends, the
:class:`.ConfigObjBackend` backend for instance uses the dots to lookup keys in nested sections.

Terminology
===========

Setting
   A definition of a key, along with some metadata, like a type or default value.

Config
   A Setting that has been configured, by specifying value.

Key
   A Setting defines a key, which can later be used to set a Config value. A key is defined as a simple ascii only
   string. A key may contain dots, which are interpreted a sections. `app.database.username` is a typical example.

Backend
   A source of Config values. Also see :ref:`supported-backends`.

prefix
   Some backends may allow a prefix to be configured. :class:`.EnvBackend` for example prepends this to the environment
   it tries to read.
