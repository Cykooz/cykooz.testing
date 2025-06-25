**************
cykooz.testing
**************

cykooz.testing is collection of helper utilities for testing.

Utilities
*********

Dict
====

A dict object that can be compared with another dict object
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

DictCi
======

A dict object that can be compared with another dict object
without regard to keys that did not present in the ``DictCi`` instance
and with case-insensitive comparison of string keys.

    >>> from cykooz.testing import DictCi
    >>> expected = DictCi({'Content-type': 1, 'user-Agent': 'foo'})
    >>> d1 = {'content-Type': 1, 'User-agent': 'foo', 'c': True}
    >>> d1 == expected
    True
    >>> expected == d1
    True
    >>> d1 != expected
    False
    >>> d2 = {'content-Type': 1, 'c': True}
    >>> d2 == expected
    False
    >>> expected == d2
    False
    >>> d1 != d2
    True
    >>> DictCi({'Content-type': 1})
    DictCi({'content-type': 1})

Short alias:

.. code-block:: python

    >>> from cykooz.testing import DCI
    >>> {'content-Type': 1, 'b': 'foo'} == DCI({'Content-type': 1})
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

Short alias:

.. code-block:: python

    >>> from cykooz.testing import J
    >>> '{"bar": "hello", "foo": 1}' == J({'foo': 1, 'bar': 'hello'})
    True

CiStr
=====

An instance of this class is compared with strings case-insensitively.

.. code-block:: python

    >>> from cykooz.testing import CiStr
    >>> v = CiStr('Content-Type')
    >>> other = 'content-type'
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
    >>> v == 'user-agent'
    False
    >>> 'user-agent' == v
    False
    >>> v != 'user-agent'
    True
    >>> v
    <CiStr: 'content-type'>
    >>> {v: 1}
    {<CiStr: 'content-type'>: 1}
    >>> [v, v, v] == [other, 2, 'user-agent']
    False
    >>> [v, v, v] == [other, other, other]
    True

Short alias:

.. code-block:: python

    >>> from cykooz.testing import CI
    >>> 'Content-Type' == CI('content-type')
    True

RoundFloat
==========

An instance of this class is compared with floats rounded to
given precision in decimal digits.

.. code-block:: python

    >>> from cykooz.testing import RoundFloat
    >>> v = RoundFloat(1.23456789, 3)
    >>> v
    <RoundFloat: 1.235>
    >>> other = 1.2347
    >>> v == other
    True
    >>> other == v
    True
    >>> other != v
    False
    >>> v == 1.2341
    False
    >>> 1.2341 == v
    False
    >>> v != 1.2341
    True
    >>> v == 1
    False
    >>> v == 'str'
    False
    >>> 'str' == v
    False
    >>> v != 'str'
    True
    >>> {v: 1}
    {<RoundFloat: 1.235>: 1}
    >>> [v, v, v] == [other, 2, 'str']
    False
    >>> [v, v, v] == [other, other, other]
    True

Short alias:

.. code-block:: python

    >>> from cykooz.testing import RF
    >>> 1.23456789 == RF(1.235, 3)
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
