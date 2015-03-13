.. streams documentation master file, created by
   sphinx-quickstart on Fri Mar 13 14:10:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to streams's documentation!
===================================

Contents:

.. toctree::
   :maxdepth: 2

.. autoclass:: streams.Stream
   :members:

Examples
--------

A basic (and rather uninteresting) stream::

    >>> for x in Stream(range(3)):
    ...     print(x)
    0
    1
    2

Streams offer various operations as methods. For example getting first 10 even integers::

    >>> from itertools import count
    >>> Stream(count()).filter(lambda x: x % 2 == 0)[:10].to_list()
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

Slicing endless iterators is supported by default.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

