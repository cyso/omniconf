omniconf
========

.. image:: https://img.shields.io/travis/cyso/omniconf.svg?maxAge=900
   :alt: Travis build status
   :target: https://travis-ci.org/cyso/omniconf

.. image:: https://img.shields.io/coveralls/cyso/omniconf.svg?maxAge=900
   :alt: Coveralls
   :target: https://coveralls.io/github/cyso/omniconf

.. image:: https://img.shields.io/pypi/l/omniconf.svg?maxAge=900
   :alt: License
   :target: https://pypi.python.org/pypi/omniconf

.. image:: https://img.shields.io/pypi/v/omniconf.svg?maxAge=900
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/omniconf

.. image:: https://img.shields.io/pypi/pyversions/omniconf.svg?maxAge=900
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/omniconf

.. image:: https://img.shields.io/pypi/implementation/omniconf.svg?maxAge=900
   :alt: Supported Python implementations
   :target: https://pypi.python.org/pypi/omniconf

A Python library that makes configuring your application independent from your configuration backend.

Documentation
-------------

Read the complete documentation on `Read the Docs <http://omniconf.readthedocs.io/en/latest/>`_.

Why omniconf?
-------------

Configuring applications is hard, and it doesn't help that there are many different (and valid) ways to do it:

* cli arguments
* config files: ConfigObj (.ini like), JSON, YAML
* environment variables
* key/value stores: etcd, consul, vault

Each of this methods are a valid way to configure an application, and each have their own strengths. Cli arguments are
most suited for tools and daemons. Configuration files are suited for applications that have more complex requirements.
Environment variables and key/value stores are handy when using containers. You may even want to use a combination of
methods (not yet implemented).

This library aims to make configuring the application easier, and allows you to use multiple configuration backends
transparently.

For up-to-date examples, take a look `here <http://omniconf.readthedocs.io/en/latest/examples.html>`_.

Changes
-------

For an up-to-date changelog, see `ChangeLog`_.

.. _ChangeLog: ChangeLog

Support for Python 3.3 was dropped in version 1.3.0 .
Support for Python 3.8 was added in version 1.3.1 .

License
-------

omniconf is licensed under LGPLv3. See the LICENSE file for details.


Contributing
------------

To contribute, base your changes on the develop branch. Make sure your contribution doesn't break any existing tests,
and add relevant new tests.

You can run the test suite using tox, which by default will run tests for all supported Python versions. You probably
want to run just a few of them at a time, use the -e switch for that:

.. code-block:: bash

   $ tox -e py27
   $ tox -e py34

To check for style issues, run flake8:

.. code-block:: bash

   $ tox -e flake8

When you're done, open a pull request on Github.
