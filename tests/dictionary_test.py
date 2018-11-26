from koalanlp import *
from koalanlp.types import *
from koalanlp.proc import *
import pytest
import inspect

Util.initialize(KKMA="2.0.2", OKT="2.0.2")
dict1 = Dictionary(API.KKMA)
dict2 = Dictionary(API.OKT)


def test_add_user_dictionary():
    dict1.addUserDictionary(("설빙", POS.NNP))
    assert dict1.contains("설빙", POS.NNP)

    dict1.addUserDictionary(("설국열차", POS.NNP), ("안드로이드", POS.NNP))
    assert dict1.contains("안드로이드", POS.NNP)
    assert dict1.contains("설국열차", POS.NNP)


def test_get_not_exists():
    assert len(dict2.getNotExists(True, ("쓰국", POS.NNP), ("일", POS.NNG))) == 1


def test_base_entries_of():
    gen = dict1.getBaseEntries(POS.isNoun)
    assert inspect.isgenerator(gen)


def test_import_from():
    try:
        dict2.importFrom(dict1, True, POS.isNoun)
    except Exception:
        raise Exception()
