#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import List, Dict, Tuple, Optional
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, launch_gateway, \
    DEFAULT_PYTHON_PROXY_PORT
from py4j.java_collections import JavaArray
from py4j.protocol import Py4JJavaError as JavaError

_CLASS_DIC = {}
GATEWAY = None


def is_jvm_running():
    global GATEWAY
    return GATEWAY is not None


def start_jvm(option, classpath, port: int = None):
    import os
    global GATEWAY

    jarpath = None
    for path in classpath:
        if 'py4j' in path:
            jarpath = path
            break

    gateway_port = launch_gateway(jarpath=jarpath, classpath=os.pathsep.join(classpath), javaopts=option)
    logging.info("Java gateway started with port number %s", gateway_port)

    if port is None:
        port = DEFAULT_PYTHON_PROXY_PORT
    logging.info("Callback server will use port number %s", port)
    GATEWAY = JavaGateway(gateway_parameters=GatewayParameters(port=gateway_port, auto_close=True),
                          callback_server_parameters=CallbackServerParameters(port=port))
    return is_jvm_running()


def check_jvm():
    class_of('java.lang.String')('123')


def shutdown_jvm():
    global GATEWAY
    global _CLASS_DIC
    from gc import collect

    # Shutdown gateway
    GATEWAY.shutdown()
    GATEWAY = None

    # Remove cached class dictionary
    _CLASS_DIC.clear()

    # Execute garbage collection
    collect()
    return is_jvm_running()


def class_of(*path):
    global GATEWAY

    strpath = '.'.join(path)
    level = GATEWAY.jvm

    if strpath not in _CLASS_DIC:
        for package in path:
            level = level.__getattr__(package)

        _CLASS_DIC[strpath] = level

    return _CLASS_DIC[strpath]


def koala_class_of(*path):
    return class_of('kr.bydelta.koala', *path)


def koala_enum_of(tagset, tag):
    return koala_class_of(tagset).valueOf(tag) if tag is not None else None


def cast_of(obj, *path):
    # Py4j does not require explicit casting.
    return obj
    # if obj is None:
    #     return None
    #
    # from jnius import cast
    # return cast('.'.join(path), obj)


def koala_cast_of(obj, *path):
    return cast_of(obj, 'kr.bydelta.koala', *path)


def string(s: str):
    return class_of('java.lang.String')(s) if s is not None else None


def py_list(result, item_converter) -> List:
    if result is None:
        return []

    if type(result) is JavaArray:
        items = []

        length = len(result)
        for i in range(length):
            items.append(result[i])

        result = items
    elif type(result) is not list:
        items = []

        it = result.iterator()
        while it.hasNext():
            items.append(it.next())

        result = items

    return [item_converter(item) for item in result]


def py_triple(result) -> Optional[Tuple]:
    if result is None:
        return None

    return result.getFirst(), result.getSecond(), result.getThird()


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
    global GATEWAY

    class PyPOSFilter(object):
        def __init__(self, gateway):
            self.gateway = gateway

        def invoke(self, tag):
            return koala_cast_of(tag, 'POS').name() in pos_set

        class Java:
            implements = ['kotlin.jvm.functions.Function1']

    return PyPOSFilter(GATEWAY)


def java_varargs(pylist, java_class):
    global GATEWAY

    varargs = GATEWAY.new_array(java_class, len(pylist))
    for i, item in enumerate(pylist):
        varargs[i] = item

    return varargs


def error_handler(e: JavaError):
    string = str(e)
    if 'NoClassDefFoundError' in string or \
            'ClassNotFoundException' in string or \
            'NoSuchMethodException' in string:
        logging.exception('Java와 통신 중에 필요한 클래스가 없다는 것을 확인했습니다. '
                          '자바 Jar 파일을 강제로 다시 다운로드하는 것을 추천합니다. '
                          '처음 initialize() 함수를 호출하실 때, force_download=True를 추가해주세요.\n'
                          '(예) initialize(KKMA="LATEST", force_download=True).\n'
                          '이렇게 해도 문제가 계속된다면, Issue를 등록해주세요.', exc_info=e)
    else:
        logging.exception('Java에서 처리하던 중에 문제가 발생했습니다. '
                          '문제가 계속된다면, Issue를 등록해주세요.', exc_info=e)
    raise e


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
    'py_triple',
    'java_list',
    'java_tuple',
    'java_triple',
    'java_set',
    'java_pos_filter',
    'java_varargs',
    'is_jvm_running',
    'start_jvm',
    'check_jvm',
    'shutdown_jvm',
    'error_handler',
    'JavaError'
]
