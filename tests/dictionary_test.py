from koalanlp import *
from koalanlp.types import *
from koalanlp.proc import *
import pytest
import inspect


@pytest.fixture(scope="session")
def dicts():
    Util.initialize(KKMA="LATEST", OKT="LATEST")
    yield Dictionary(API.KKMA), Dictionary(API.OKT)
    Util.finalize()


def test_add_user_dictionary(dicts):
    dict1, dict2 = dicts
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


def test_get_not_exists(dicts):
    dict1, dict2 = dicts
    assert len(dict2.getNotExists(True, ("쓰국", POS.NNP), ("일", POS.NNG))) == 1


def test_base_entries_of(dicts):
    dict1, dict2 = dicts
    gen = dict1.getBaseEntries(lambda t: t.isNoun())
    assert inspect.isgenerator(gen)
    assert next(gen) is not None
    gen = list(gen)

    gen2 = dict1.getBaseEntries(lambda t: t.isAffix())
    assert inspect.isgenerator(gen2)
    gen2 = list(gen2)
    assert len(gen2) > 0

    counter = 0
    for entry in gen:
        counter += (entry in gen2)
    assert counter == 0


def test_import_from(dicts):
    dict1, dict2 = dicts
    item_sz_prev = len(dict2.getItems())
    item_noun_prev = sum(1 for _, p in dict2.getItems() if p.isNoun())

    dict2.importFrom(dict1, True, lambda t: t.isNoun())

    item_sz_after = len(dict2.getItems())
    item_noun_after = sum(1 for _, p in dict2.getItems() if p.isNoun())
    assert item_sz_prev < item_sz_after
    assert item_sz_after - item_sz_prev == item_noun_after - item_noun_prev
