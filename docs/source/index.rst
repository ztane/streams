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

A basic stream::

    >>> for x in Stream(range(3)):
    ...     print(x)
    0
    1
    2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

