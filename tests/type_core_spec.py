from koalanlp import *
from koalanlp.types import *
import pytest
import random


@pytest.fixture(scope="session")
def jvm():
    Util.initialize(CORE="LATEST")
    yield None
    Util.finalize()


def test_POS_discriminate_tags(jvm):
    SET_NOUNS = lambda x: x.isNoun()
    SET_PREDICATES = lambda x: x.isPredicate()
    SET_MODIFIERS = lambda x: x.isModifier()
    SET_POSTPOSITIONS = lambda x: x.isPostPosition()
    SET_ENDINGS = lambda x: x.isEnding()
    SET_AFFIXES = lambda x: x.isAffix()
    SET_SUFFIXES = lambda x: x.isSuffix()
    SET_SYMBOLS = lambda x: x.isSymbol()
    SET_UNKNOWNS = lambda x: x.isUnknown()

    map = {
        'NNG': {SET_NOUNS},
        'NNP': {SET_NOUNS},
        'NNB': {SET_NOUNS},
        'NNM': {SET_NOUNS},
        'NR': {SET_NOUNS},
        'NP': {SET_NOUNS},
        'VV': {SET_PREDICATES},
        'VA': {SET_PREDICATES},
        'VX': {SET_PREDICATES},
        'VCP': {SET_PREDICATES},
        'VCN': {SET_PREDICATES},
        'MM': {SET_MODIFIERS},
        'MAG': {SET_MODIFIERS},
        'MAJ': {SET_MODIFIERS},
        'IC': set(),
        'JKS': {SET_POSTPOSITIONS},
        'JKC': {SET_POSTPOSITIONS},
        'JKG': {SET_POSTPOSITIONS},
        'JKO': {SET_POSTPOSITIONS},
        'JKB': {SET_POSTPOSITIONS},
        'JKV': {SET_POSTPOSITIONS},
        'JKQ': {SET_POSTPOSITIONS},
        'JC': {SET_POSTPOSITIONS},
        'JX': {SET_POSTPOSITIONS},
        'EP': {SET_ENDINGS},
        'EF': {SET_ENDINGS},
        'EC': {SET_ENDINGS},
        'ETN': {SET_ENDINGS},
        'ETM': {SET_ENDINGS},
        'XPN': {SET_AFFIXES},
        'XPV': {SET_AFFIXES},
        'XSN': {SET_AFFIXES, SET_SUFFIXES},
        'XSV': {SET_AFFIXES, SET_SUFFIXES},
        'XSA': {SET_AFFIXES, SET_SUFFIXES},
        'XSM': {SET_AFFIXES, SET_SUFFIXES},
        'XSO': {SET_AFFIXES, SET_SUFFIXES},
        'XR': set(),
        'SF': {SET_SYMBOLS},
        'SP': {SET_SYMBOLS},
        'SS': {SET_SYMBOLS},
        'SE': {SET_SYMBOLS},
        'SO': {SET_SYMBOLS},
        'SW': {SET_SYMBOLS},
        'NF': {SET_UNKNOWNS},
        'NV': {SET_UNKNOWNS},
        'NA': {SET_UNKNOWNS},
        'SL': set(),
        'SH': set(),
        'SN': set()
    }

    tagset = [SET_UNKNOWNS,
              SET_SYMBOLS,
              SET_SUFFIXES,
              SET_AFFIXES,
              SET_ENDINGS,
              SET_POSTPOSITIONS,
              SET_MODIFIERS,
              SET_PREDICATES,
              SET_NOUNS]

    assert set(map.keys()) == {it.name for it in POS.values() if it.name != 'TEMP'}

    for tag, setup in map.items():
        for target in tagset:
            assert target(getattr(POS, tag)) == (target in setup)
            assert getattr(POS, tag) == POS.valueOf(tag)


def test_POS_startsWith(jvm):
    partialCodes = set()
    for tag in POS.values():
        if tag != POS.TEMP:
            name = tag.name

            for l in range(1, len(name) + 1):
                partialCodes.add(name[:l])
                partialCodes.add(name[:l].lower())

    for tag in POS.values():
        if tag != POS.TEMP:
            if tag.isUnknown():
                for code in partialCodes:
                    if code.upper() == 'N':
                        assert not tag.startsWith(code)
                    else:
                        assert tag.startsWith(code) == tag.name.startswith(code.upper())
            else:
                for code in partialCodes:
                    assert tag.startsWith(code) == tag.name.startswith(code.upper())


def test_PhraseTag_ExtUtil(jvm):
    values = PhraseTag.values()
    codes = {it.name for it in values}

    for _ in range(100):
        filtered = [code for code in codes if random.random() > 0.5]

        for tag in values:
            assert Util.contains(filtered, tag) == (tag.name in filtered)

    for code in codes:
        assert PhraseTag.valueOf(code) == getattr(PhraseTag, code)


def test_DepTag_ExtUtil(jvm):
    values = DependencyTag.values()
    codes = {it.name for it in values}

    for _ in range(100):
        filtered = [code for code in codes if random.random() > 0.5]

        for tag in values:
            assert Util.contains(filtered, tag) == (tag.name in filtered)

    for code in codes:
        assert DependencyTag.valueOf(code) == getattr(DependencyTag, code)


def test_RoleType_ExtUtil(jvm):
    values = RoleType.values()
    codes = {it.name for it in values}

    for _ in range(100):
        filtered = [code for code in codes if random.random() > 0.5]

        for tag in values:
            assert Util.contains(filtered, tag) == (tag.name in filtered)

    for code in codes:
        assert RoleType.valueOf(code) == getattr(RoleType, code)


def test_CET_ExtUtil(jvm):
    values = CoarseEntityType.values()
    codes = {it.name for it in values}

    for _ in range(100):
        filtered = [code for code in codes if random.random() > 0.5]

        for tag in values:
            assert Util.contains(filtered, tag) == (tag.name in filtered)

    for code in codes:
        assert CoarseEntityType.valueOf(code) == getattr(CoarseEntityType, code)
