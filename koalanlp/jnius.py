#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict

_CLASS_DIC = {}


def class_of(*path):
    from jnius import autoclass
    path = '.'.join(path)

    if path not in _CLASS_DIC:
        _CLASS_DIC[path] = autoclass(path)

    return _CLASS_DIC[path]


def koala_class_of(*path):
    return class_of('kr.bydelta.koala', *path)


def koala_enum_of(tagset, tag):
    return koala_class_of(tagset).valueOf(tag) if tag is not None else None


def cast_of(obj, *path):
    if obj is None:
        return None

    from jnius import cast
    return cast('.'.join(path), obj)


def koala_cast_of(obj, *path):
    return cast_of(obj, 'kr.bydelta.koala', *path)


def string(s: str):
    return class_of('java.lang.String')(s.encode('UTF-8')) if s is not None else None


def py_list(result, item_converter) -> List:
    if result is None:
        return []

    if type(result) is not list:
        items = []

        it = result.iterator()
        while it.hasNext():
            items.append(it.next())

        result = items

    return [item_converter(item) for item in result]


def py_dict(result, key_converter=None, value_converter=None) -> Dict:
    dic = {}
    keys = result.keySet().toArray()

    for key in keys:
        py_key = key_converter(key) if key_converter is not None else key
        py_value = result.get(key)
        py_value = value_converter(py_value) if value_converter is not None else py_value

        dic[py_key] = py_value

    return dic


def java_list(pylist: List):
    array_list = class_of('java.util.ArrayList')()

    for item in pylist:
        array_list.add(item)

    return array_list


def java_tuple(first, second):
    return class_of('kotlin.Pair')(first, second)


def java_triple(first, second, third):
    return class_of('kotlin.Triple')(first, second, third)


def java_set(pylist):
    hash_set = class_of('java.util.HashSet')()

    for item in pylist:
        hash_set.add(item)

    return hash_set


def java_pos_filter(pos_set):
    from jnius import PythonJavaClass, java_method

    class PyPOSFilter(PythonJavaClass):
        __javainterfaces__ = ['kotlin/jvm/functions/Function1']

        def __init__(self):
            super().__init__()

        @java_method('(Lkr/bydelta/koala/POS;)Z', name='invoke')
        def invoke(self, method, tag):
            return tag in pos_set

    return PyPOSFilter()


# ----- Define members exported -----

__all__ = [
    'class_of',
    'koala_class_of',
    'koala_enum_of',
    'cast_of',
    'koala_cast_of',
    'string',
    'py_list',
    'py_dict',
    'java_list',
    'java_tuple',
    'java_triple',
    'java_set',
    'java_pos_filter',
]
