.. _setting-types:

Setting types
=============

When a :class:`.Setting` is defined, a type is also declared. By default, the value of a `Setting`
is :class:`str`, but any class or function that accepts a single parameter and returns a class instance can be
used. The class or function passed to `_type` will be called with the value to process as its only parameter.

Built-in interpretation
-----------------------

Special cases are added to support :class:`dict`, :class:`list`, :func:`tuple` and :class:`bool`, which are
processed by :mod:`ast`. The implementation can be found in the ``unrepr`` method in ``omniconf.config``:

.. autofunction :: omniconf.config.unrepr

This means that a `Setting` declared as such:

.. code-block:: python

   from omniconf import setting
   setting("items", _type=list)


Which is provided by a backend with the following string:

.. code-block:: python

   "['foo', 'bar', 'baz']"

Will return a list that looks like this:

.. code-block:: python

   from omniconf import config
   print(config("items"))
   # ['foo', 'bar', 'baz']


For detailed information, see the :mod:`ast` documentation.

Custom interpretation and types
-------------------------------

The most simple custom type looks like this:

.. code-block:: python

   def custom_type(src):
      return src

This example simply takes the input as provided, and returns it as-is. Custom types are not limited to functions,
classes can also be used. Any class that has exactly one (mandatory) parameter is valid):

.. code-block:: python

   class CustomType(object):
      def __init__(self, src, foo=bar):
         self.src = src

Some custom types are provided with |project|, which may be used as-is, but also serve as examples.

Separator Sequence
^^^^^^^^^^^^^^^^^^

A somewhat fancy name for what one might normally call a comma separated list. The implementation is not
limited to just commas however, and can use any string.

.. autofunction :: omniconf.types.separator_sequence
.. autoclass :: omniconf.types.SeparatorSequence
