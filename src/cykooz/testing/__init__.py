# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 19.11.2015
"""

import json
import re


__all__ = (
    'Url',
    'Dict',
    'D',
    'DictCi',
    'DCI',
    'List',
    'L',
    'AnyValue',
    'ANY',
    'RegExpString',
    'R',
    'Json',
    'J',
    'CiStr',
    'CI',
    'RoundFloat',
    'RF',
)

from urllib.parse import urlparse, parse_qsl, unquote_plus


class Url:
    """A url object that can be compared with other url objects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings.

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
    """

    __slots__ = ('parts',)

    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        if not isinstance(other, Url):
            other = Url(other)
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)


class Dict(dict):
    """A dict object that can be compared with another dict object
    without regard to keys that did not present in the ``Dict`` instance.

        >>> expected = Dict(a=1, b='foo')
        >>> d1 = {'a': 1, 'b': 'foo', 'c': True}
        >>> d1 == expected
        True
        >>> expected == d1
        True
        >>> d1 != expected
        False
        >>> d2 = {'a': 1, 'c': True}
        >>> d2 == expected
        False
        >>> expected == d2
        False
        >>> d1 != d2
        True
        >>> Dict({'a': 1})
        Dict({'a': 1})
    """

    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        for key, value in self.items():
            if key not in other:
                return False
            if value != other[key]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Dict(%s)' % super(Dict, self).__repr__()


class DictCi(Dict):
    """A dict object that can be compared with another dict object
    without regard to keys that did not present in the ``DictCi`` instance
    and with case-insensitive comparison of string keys.

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
    """

    def __init__(self, *args, **kwargs):
        super(DictCi, self).__init__(*args, **kwargs)
        for key, value in list(self.items()):
            if isinstance(key, str):
                l_key = key.lower()
                if l_key != key:
                    self[l_key] = value
                    del self[key]

    def __eq__(self, other):
        other_ci = {}
        for key, value in other.items():
            if isinstance(key, str):
                key = key.lower()
            other_ci[key] = value
        return super().__eq__(other_ci)

    def __repr__(self):
        return 'DictCi(%s)' % super(Dict, self).__repr__()


class List(list):
    """A list object that can be compared with other list object
    without regard to extra items contains in the other list object.

        >>> expected = List([1, 'foo'])
        >>> l1 = [1, 'foo', True]
        >>> l1 == expected
        True
        >>> expected == l1
        True
        >>> l1 != expected
        False
        >>> l2 = [1, True]
        >>> l2 == expected
        False
        >>> expected == l2
        False
        >>> l2 != expected
        True
        >>> expected == [1]
        False
        >>> List([1, 'foo', True])
        List([1, 'foo', True])
        >>> [{'a': 1}, {'b': 2}] == List([Dict(), Dict()])
        True
        >>> expected = List([True, 1], ignore_order=True)
        >>> expected
        List([True, 1], ignore_order=True)
        >>> l3 = [1, 'foo', True]
        >>> l3 == expected
        True
        >>> l3 != expected
        False
        >>> [{'a': 1}, {'b': 2}] == List([Dict(), Dict()], ignore_order=True)
        Traceback (most recent call last):
        ...
        TypeError: unhashable type: 'Dict'
    """

    def __init__(self, *args, ignore_order=False, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.ignore_order = ignore_order

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        if len(self) > len(other):
            return False
        if self.ignore_order:
            return len(set(self) - set(other)) == 0
        for v1, v2 in zip(self, other):
            if v1 != v2:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        suffix = ''
        if self.ignore_order:
            suffix = ', ignore_order=True'
        return 'List(%s%s)' % (super(List, self).__repr__(), suffix)


class AnyValue:
    """Instance of this class is equal to any other values.

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
    """

    __hash__ = None

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    def __repr__(self):
        return '<any value>'


class RegExpString:
    """Instance of this class is equal to any other values if it is matched to give regexp pattern.

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
    """

    def __init__(self, pattern, flags=re.UNICODE):
        self.pattern = pattern
        self.re = re.compile(pattern, flags)

    __hash__ = None

    def __eq__(self, other):
        if isinstance(other, bytes):
            other = other.decode('utf-8')
        elif not isinstance(other, str):
            other = str(other)
        return bool(self.re.match(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<RegExpString: %s>' % self.pattern


class Json:
    """An instance of this class will be equal to any 'bytes' or 'str' value
    if object decoded by JSON-decoder from this value is equal to the first
    argument of this class.

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
    """

    def __init__(self, value, **kwargs):
        self.value = value
        self.kwargs = kwargs

    __hash__ = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

        if isinstance(other, bytes):
            try:
                other = other.decode('utf-8')
            except UnicodeDecodeError:
                return False

        if isinstance(other, str):
            try:
                other = json.loads(other, **self.kwargs)
                return self.value == other
            except ValueError:
                pass

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<Json: %r>' % self.value


class CiStr:
    """An instance of this class is compared with strings case-insensitively.

    >>> v = CiStr('Content-type')
    >>> other = 'content-Type'
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
    >>> list_values = [other, 2, 'user-agent']
    >>> [v, v, v] == list_values
    False
    >>> v in list_values
    True
    >>> v in set(list_values)
    False
    >>> v in {other: 1}
    False
    >>> [v, v, v] == [other, other, other]
    True
    """

    __slots__ = ('value',)

    def __init__(self, value):
        self.value = str(value).lower()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        if isinstance(other, str):
            other = other.lower()
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<CiStr: %r>' % self.value


class RoundFloat:
    """An instance of this class is compared with floats rounded to
    given precision in decimal digits.

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
    """

    __slots__ = ('value', 'ndigits')

    def __init__(self, value: int | float, ndigits: int):
        self.value = round(value, ndigits)
        self.ndigits = ndigits

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        if isinstance(other, (int, float)):
            other = round(other, self.ndigits)
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<RoundFloat: %r>' % self.value


# Short aliases
ANY = AnyValue()
D = Dict
DCI = DictCi
L = List
R = RegExpString
J = Json
CI = CiStr
RF = RoundFloat
