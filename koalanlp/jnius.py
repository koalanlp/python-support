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


def string(s: str):
    return class_of('java.lang.String')(s.encode('UTF-8'))


def char(s: str):
    if s is not None:
        return class_of('java.lang.String')(s.encode('UTF-8')).get(0)
    else:
        return None


def py_str(item) -> str:
    return item.toString()


def py_list(result, item_converter) -> List:
    if result is None:
        return []

    return [item_converter(item) for item in result]


def py_dict(result, key_converter=None, value_converter=None) -> Dict:
    dic = {}
    keys = result.keys()

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


def java_set(pylist):
    hash_set = class_of('java.util.HashSet')()

    for item in pylist:
        hash_set.add(item)

    return hash_set


def java_pos_filter(pos_set):
    from jnius import PythonJavaClass, java_method

    class PyPOSFilter(PythonJavaClass):
        __javainterfaces__ = ['java/util/function/Function']

        def __init__(self):
            super().__init__()

        @java_method('(Lkr/bydelta/koala/POS)Z')
        def apply(self, tag):
            return tag in pos_set

    return PyPOSFilter()


# ----- Define members exported -----

__all__ = [
    'class_of',
    'koala_class_of',
    'string',
    'char',
    'py_str',
    'py_list',
    'py_dict',
    'java_list',
    'java_tuple',
    'java_set',
    'java_pos_filter',
]
