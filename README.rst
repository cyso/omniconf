omniconf
========

.. image:: https://img.shields.io/travis/cyso/omniconf.svg?maxAge=2592000
   :alt: Travis build status
   :target: https://travis-ci.org/cyso/omniconf

.. image:: https://img.shields.io/coveralls/cyso/omniconf.svg?maxAge=2592000
   :alt: Coveralls
   :target: https://coveralls.io/github/cyso/omniconf

.. image:: https://img.shields.io/pypi/l/omniconf.svg?maxAge=2592000
   :alt: License
   :target: https://pypi.python.org/pypi/omniconf

.. image:: https://img.shields.io/pypi/v/omniconf.svg?maxAge=2592000
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/omniconf

.. image:: https://img.shields.io/pypi/pyversions/omniconf.svg?maxAge=2592000
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/omniconf

A Python library that makes configuring your application independent from your configuration backend.

Documentation
-------------

Read the documentation on `Read the Docs <http://omniconf.readthedocs.io/en/latest/>`_.

Design choices
--------------

Configuring applications is hard, and it doesn't help that there are many different (and valid) ways to do it:

* cli arguments
* config files: ConfigObj (.ini like), JSON, YAML
* environment variables
* key/value stores: etcd, consul (not yet implemented).

Each of this methods are a valid way to configure an application, and each have their own strengths. Cli arguments are most suited for tools and daemons. Configuration files are suited for applications that have more complex requirements. Environment variables and key/value stores are handy when using containers. You may even want to use a combination of methods (not yet implemented).

This library aims to make configuring the application easier, and allows you to use multiple configuration backends transparently.

To do this, configuration keys are defined as simple key / value pairs:

.. code-block:: ini

   key=value

Sections and subsections are also supported, by using dot notated syntax:

.. code-block:: ini

   section.subsection.key=value

To use a configuration key in your application, simply use:

.. code-block:: python

   from omniconf import config

   variable = config.get("section.key")

`omniconf` needs to be told what keys to expect, define these as follows:

.. code-block:: python

   from omniconf import setting
   # Simplest way to define a key
   setting('key')

   # A more complex example
   setting('section.subsection.key', _type=dict, default={"foo": "bar"}, help="This is a very import key")

License
-------

omniconf is licensed under LGPLv3. See the LICENSE file for details.


Contributing
------------

To contribute, base your changes on the develop branch. Make sure your contribution doesn't break any existing tests, and add relevant new tests.

You can run the test suite using tox, which by default will run tests for all supported Python versions. You probably want to run just a few of them at a time, use the -e switch for that:

.. code-block:: bash

   $ tox -e py27
   $ tox -e py34

To check for style issues, run flake8:

.. code-block:: bash

   $ tox -e flake8

When you're done, open a pull request on Github.
