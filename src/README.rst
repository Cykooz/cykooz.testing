**************
cykooz.testing
**************

cykooz.testing is collection of helper utilities for testing.

Utilities
*********

Dict
====

A dict object that can be compared with other dict object
without regard to keys that did not presents in the ``Dict`` instance.

.. code-block:: python

    >>> from cykooz.testing import Dict
    >>> d1 = Dict(a=1, b='foo')
    >>> d2 = {'a': 1, 'b': 'foo', 'c': True}
    >>> d1 == d2
    True
    >>> d2 == d1
    True
    >>> d1 != d2
    False
    >>> d3 = {'a': 1, 'c': True}
    >>> d1 == d3
    False
    >>> d3 == d1
    False
    >>> d1 != d3
    True
    >>> Dict({'a': 1})
    Dict({'a': 1})

Short alias:

.. code-block:: python

    >>> from cykooz.testing import D
    >>> {'a': 1, 'b': 'foo'} == D({'a': 1})
    True

List
====

A list object that can be compared with other list object
without regard to extra items contains in the other list object.

.. code-block:: python

    >>> from cykooz.testing import List
    >>> l1 = List([1, 'foo'])
    >>> l2 = [1, 'foo', True]
    >>> l1 == l2
    True
    >>> l2 == l1
    True
    >>> l1 != l2
    False
    >>> l3 = [1, True]
    >>> l1 == l3
    False
    >>> l3 == l1
    False
    >>> l1 != l3
    True
    >>> l1 == [1]
    False
    >>> List([1, 'foo', True])
    List([1, 'foo', True])
    >>> List([Dict(), Dict()]) == [{'a': 1}, {'b': 2}]
    True

Short alias:

.. code-block:: python

    >>> from cykooz.testing import L
    >>> [1, 'foo', True] == L([1, 'foo'])
    True

AnyValue
========

Instance of this class is equal to any other values.

.. code-block:: python

    >>> from cykooz.testing import AnyValue
    >>> v = AnyValue()
    >>> v == 1
    True
    >>> 1 == v
    True
    >>> v != 1
    False
    >>> v == {'a': 1, 'b': 'foo'}
    True
    >>> v == [1, 2, 3, 'b']
    True
    >>> v == AnyValue()
    True
    >>> v
    <any value>
    >>> {v: 1}
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'AnyValue'
    >>> [v, v, v] == [1, 2, 'foo']
    True
    >>> [v, v, 1] == [1, 2, 'foo']
    False
    >>> [v, v] == [1, 2, 'foo']
    False
    >>> {'a': v, 'b': 2} == {'a': 1, 'b': 2}
    True

Short alias:

.. code-block:: python

    >>> from cykooz.testing import ANY
    >>> 1 == ANY
    True

RegExpString
============

Instance of this class is equal to any other values if it is matched
to give regexp pattern.

.. code-block:: python

    >>> v = RegExpString('first.*')
    >>> v == 1
    False
    >>> 1 == v
    False
    >>> v != 1
    True
    >>> v == 'first class'
    True
    >>> 'first class' == v
    True
    >>> v != 'first class'
    False
    >>> v
    <RegExpString: first.*>
    >>> {v: 1}
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'RegExpString'
    >>> [v, v, v] == [1, 2, 'first class']
    False
    >>> [v, v, v] == ['first class', 'first bus', 'first time']
    True

Short alias:

.. code-block:: python

    >>> from cykooz.testing import R
    >>> 'first class' == R('first.*')
    True

Url
===

A url object that can be compared with other url objects
without regard to the vagaries of encoding, escaping, and ordering
of parameters in query strings.

.. code-block:: python

    >>> from cykooz.testing import Url
    >>> url1 = Url('http://domain.com/container?limit=6&offset=0')
    >>> url2 = Url('http://domain.com/container?offset=0&limit=6')
    >>> url1 == url2
    True
    >>> url2 = Url('http://domain.com/container?limit=6')
    >>> url1 == url2
    False
    >>> url1 == 'http://domain.com/container?offset=0&limit=6'
    True
    >>> 'http://domain.com/container?offset=0&limit=6' == url1
    True
    >>> {'key': 'http://domain.com/container?offset=0&limit=6'} == {'key': url1}
    True
