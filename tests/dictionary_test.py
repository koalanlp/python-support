from koalanlp import *
from koalanlp.types import *
from koalanlp.proc import *
import pytest
import inspect

Util.initialize(KKMA="LATEST", OKT="LATEST")
dict1 = Dictionary(API.KKMA)
dict2 = Dictionary(API.OKT)


def test_add_user_dictionary():
    dict1.addUserDictionary(("설빙", POS.NNP))
    assert dict1.contains("설빙", POS.NNP)

    dict1.addUserDictionary(("설국열차", POS.NNP), ("안드로이드", POS.NNP))
    assert dict1.contains("안드로이드", POS.NNP)
    assert dict1.contains("설국열차", POS.NNP)

    dict1.addUserDictionary(("하동균", POS.NNP))
    dict1.addUserDictionary(("나비야", POS.NNP))

    assert dict1.contains("하동균", POS.NNP, POS.NNG)
    assert ("하동균", POS.NNP) in dict1

    assert len(list(dict1.getItems())) == 5


def test_get_not_exists():
    assert len(dict2.getNotExists(True, ("쓰국", POS.NNP), ("일", POS.NNG))) == 1


def test_base_entries_of():
    gen = dict1.getBaseEntries(POS.isNoun)
    assert inspect.isgenerator(gen)
    assert next(gen) is not None

    gen = dict1.getBaseEntries(lambda t: t.isAffix())
    assert inspect.isgenerator(gen)
    assert len(list(gen)) > 0


def test_import_from():
    try:
        item_sz_prev = len(dict2.getItems())
        dict2.importFrom(dict1, True, POS.isNoun)
        assert item_sz_prev < len(dict2.getItems())
    except Exception:
        raise Exception()
