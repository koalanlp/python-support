from koalanlp import *
import pytest
import inspect

initialize([API.TWITTER, API.EUNJEON], "1.9.2")
dict1 = Dictionary(API.TWITTER)
dict2 = Dictionary(API.EUNJEON)

def test_add_user_dictionary():
    dict1.add_user_dictionary("설빙", POS.NNP)
    assert dict1.contains("설빙", POS.NNP)

    dict1.add_user_dictionary(["설국열차", "안드로이드"], [POS.NNP, POS.NNP])
    assert dict1.contains("안드로이드", POS.NNP)
    assert dict1.contains("설국열차", POS.NNP)

def test_get_not_exists():
    assert len(dict2.get_not_exists(True, ("설빙", POS.NNP), ("일", POS.NNG))) == 1

def test_base_entries_of():
    gen = dict1.base_entries_of(POS.is_noun)
    assert inspect.isgenerator(gen)

def test_import_from():
    try:
        dict2.import_from(dict1, POS.is_noun, True)
    except:
        raise Exception()
