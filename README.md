omniconf
========

[![Travis build status](https://img.shields.io/travis/cyso/omniconf.svg?maxAge=2592000)](https://travis-ci.org/cyso/omniconf)
[![Coveralls](https://img.shields.io/coveralls/cyso/omniconf.svg?maxAge=2592000)](https://coveralls.io/github/cyso/omniconf)
[![License](https://img.shields.io/pypi/l/omniconf.svg?maxAge=2592000)](https://pypi.python.org/pypi/omniconf)
[![PyPI version](https://img.shields.io/pypi/v/omniconf.svg?maxAge=2592000)](https://pypi.python.org/pypi/omniconf)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/omniconf.svg?maxAge=2592000)](https://pypi.python.org/pypi/omniconf)

A Python library that makes configuring your application independent from your configuration backend.

Documentation
-------------

Read the documentation on [Read the Docs](http://omniconf.readthedocs.io/en/latest/).

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

```
key=value
```

Sections and subsections are also supported, by using dot notated syntax:

```
section.subsection.key=value
```

To use a configuration key in your application, simply use:

```python
from omniconf import config

variable = config.get("section.key")
```

`omniconf` needs to be told what keys to expect, define these as follows:

```python
from omniconf import setting
# Simplest way to define a key
setting('key')

# A more complex example
setting('section.subsection.key', _type=dict, default={"foo": "bar"}, help="This is a very import key")
```
