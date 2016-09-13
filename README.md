omniconf
========

A Python library that makes configuring your application independent from a configuration backend.

Design choices
--------------

Configuring applications is hard, and it doesn't help that there are many different (and valid) ways to do it:

* cli arguments
* config files: .ini, ConfigObj, JSON, YAML
* environment variables
* key/value stores: etcd, consul

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
from omniconf import conf

variable = conf.get("section.key")
```

`omniconf` needs to be told what keys to expect, define these as follows:

```python
from omniconf import setting
# Simplest way to define a key
setting('key')

# A more complex example
setting('section.subsection.key', _type=dict, default={"foo": "bar"}, help="This is a very import key")
```
