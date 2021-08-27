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
    >>> expected = Dict(a=1, b='foo')
    >>> d1 = {'a': 1, 'b': 'foo', 'c': True}
    >>> d1 == expected
    True
    >>> d1 != expected
    False
    >>> d2 = {'a': 1, 'c': True}
    >>> d2 == expected
    False
    >>> d1 != d2
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
    >>> expected = List([1, 'foo'])
    >>> l1 = [1, 'foo', True]
    >>> l1 == expected
    True
    >>> l1 != expected
    False
    >>> l2 = [1, True]
    >>> l2 == expected
    False
    >>> l2 != expected
    True
    >>> expected == [1]
    False
    >>> [{'a': 1}, {'b': 2}] == List([Dict(), Dict()])
    True

Also supported comparing without regard of ordering of items.

.. code-block:: python

    >>> expected = List([True, 1], ignore_order=True)
    >>> l1 = [1, 'foo', True]
    >>> l1 == expected
    True
    >>> l1 != expected
    False
    >>> [{'a': 1}, {'b': 2}] == List([Dict(), Dict()], ignore_order=True)
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'Dict'

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

    >>> from cykooz.testing import RegExpString
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
    >>> url1 = Url('https://domain.com/container?limit=6&offset=0')
    >>> url2 = Url('https://domain.com/container?offset=0&limit=6')
    >>> url1 == url2
    True
    >>> url2 = Url('https://domain.com/container?limit=6')
    >>> url1 == url2
    False
    >>> url1 == 'https://domain.com/container?offset=0&limit=6'
    True
    >>> 'https://domain.com/container?offset=0&limit=6' == url1
    True
    >>> {'key': 'https://domain.com/container?offset=0&limit=6'} == {'key': url1}
    True

Json
====

An instance of this class will be equal to any 'bytes' or 'str' value
if object decoded by JSON-decoder from this value is equal to the first
argument of this class.

.. code-block:: python

    >>> from cykooz.testing import Json
    >>> v = Json({'foo': 1, 'bar': 'hello'})
    >>> other = '{"bar": "hello", "foo": 1}'
    >>> v == other
    True
    >>> other == v
    True
    >>> other != v
    False
    >>> v == 1
    False
    >>> 1 == v
    False
    >>> v != 1
    True
    >>> v == 'not json'
    False
    >>> 'not json' == v
    False
    >>> v != 'not json'
    True
    >>> v
    <Json: {'foo': 1, 'bar': 'hello'}>
    >>> {v: 1}
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'Json'
    >>> [v, v, v] == [other, 2, 'first class']
    False
    >>> [v, v, v] == [other, other, other]
    True
    >>> '"json str"' == Json('json str')
    True

Complex example
***************

.. code-block:: python

    >>> from cykooz.testing import D, L, R, J, Url, ANY
    >>> some_value = {
    ...     'created': '2020-04-14T12:34:00.002000+00:00',
    ...     'is_active': True,
    ...     'items': [
    ...         {'key': 'a', 'value': 1},
    ...         {'key': 'b', 'value': 2},
    ...         {'key': 'c', 'value': 3},
    ...     ],
    ...     'source': 'https://domain.com/item?p=0&t=total',
    ...     'response': '{"status": 200, "body": "OK"}',
    ...     'size': 1024,
    ... }
    >>> some_value == D({
    ...     'created': R('^2020-04.*'),
    ...     'is_active': True,
    ...     'items': L([
    ...         {'key': 'a', 'value': 1},
    ...         D({'value': ANY}),
    ...     ]),
    ...     'source': Url('https://domain.com/item?t=total&p=0'),
    ...     'response': J({'status': 200, 'body': ANY}),
    ... })
    True
