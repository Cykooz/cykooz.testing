# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 19.11.2015
"""
import re

import six
from six.moves.urllib.parse import parse_qsl, unquote_plus, urlparse


__all__ = (
    'Url',
    'Dict', 'D',
    'List', 'L',
    'AnyValue', 'ANY',
    'RegExpString', 'R',
)


class Url(object):
    """A url object that can be compared with other url objects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings.

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
    """A dict object that can be compared with other dict object
    without regard to keys that did not presents in the ``Dict`` instance.

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


class List(list):
    """A list object that can be compared with other list object
    without regard to extra items contains in the other list object.

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
    """

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        if len(self) > len(other):
            return False
        for v1, v2 in zip(self, other):
            if v1 != v2:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'List(%s)' % super(List, self).__repr__()


class AnyValue(object):
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


class RegExpString(object):
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
        if isinstance(other, six.binary_type):
            other = other.decode('utf-8')
        elif not isinstance(other, six.text_type):
            other = six.text_type(other)
        return bool(self.re.match(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<RegExpString: %s>' % self.pattern


# Short aliases
ANY = AnyValue()
D = Dict
L = List
R = RegExpString
