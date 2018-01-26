#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data import Morpheme

NNG = "NNG"
NNP = "NNP"
NNB = "NNB"
NR = "NR"
NP = "NP"

VV = "VV"
VA = "VA"
VX = "VX"
VCP = "VCP"
VCN = "VCN"

MM = "MM"
MAG = "MAG"
MAJ = "MAJ"

JKS = "JKS"
JKC = "JKC"
JKG = "JKG"
JKO = "JKO"
JKB = "JKB"
JKV = "JKV"
JKQ = "JKQ"
JC = "JC"
JX = "JX"

EP = "EP"
EF = "EF"
EC = "EC"
ETN = "ETN"
ETM = "ETM"

XPN = "XPN"
XPV = "XPV"
XSN = "XSN"
XSV = "XSV"
XSM = "XSM"
XSO = "XSO"
XR = "XR"

SF = "SF"
SP = "SP"
SS = "SS"
SE = "SE"
SW = "SW"
SO = "SO"

NF = "NF"
NV = "NV"
NA = "NA"

_NOUN_SET = [NNG, NNP, NNB, NR, NP]
_PRED_SET = [VV, VA, VX, VCP, VCN]
_MODF_SET = [MM, MAG, MAJ]
_JOSA_SET = [JKS, JKC, JKG, JKO, JKB, JKV, JKQ, JC, JX]
_EOMI_SET = [EP, EF, EC, ETN, ETM]
_AFFX_SET = [XPN, XPV, XSN, XSV, XSM, XSO, XR]
_SUFX_SET = [XSN, XSV, XSM, XSO]
_SYMB_SET = [SF, SP, SS, SE, SW, SO]
_UNKN_SET = [NF, NV, NA]

TAGS = [pos for pos in dir() if not pos.startswith('_') and pos.isupper()]

def _finder(sets, tag) -> bool:
    if type(tag) is str:
        return tag in sets
    elif type(tag) is Morpheme:
        return tag.tag in sets
    else:
        return False


def is_noun(tag) -> bool:
    """
    주어진 품사표기/형태소가 체언(명사,대명사,의존명사,수사)인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 체언이면 True
    """
    return _finder(_NOUN_SET, tag)


def is_predicate(tag) -> bool:
    """
    주어진 품사표기/형태소가 용언(동사,형용사)인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 용언이면 True
    """
    return _finder(_PRED_SET, tag)


def is_modifier(tag) -> bool:
    """
    주어진 품사표기/형태소가 수식언(관형사,부사)인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 수식언이면 True
    """
    return _finder(_MODF_SET, tag)


def is_postposition(tag) -> bool:
    """
    주어진 품사표기/형태소가 관계언(조사)인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 관계언이면 True
    """
    return _finder(_JOSA_SET, tag)


def is_ending(tag) -> bool:
    """
    주어진 품사표기/형태소가 어미인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 어미이면 True
    """
    return _finder(_EOMI_SET, tag)


def is_affix(tag) -> bool:
    """
    주어진 품사표기/형태소가 접사인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 접사이면 True
    """
    return _finder(_AFFX_SET, tag)


def is_suffix(tag) -> bool:
    """
    주어진 품사표기/형태소가 접미사인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 접미사이면 True
    """
    return _finder(_SUFX_SET, tag)


def is_symbol(tag) -> bool:
    """
    주어진 품사표기/형태소가 기호인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 기호이면 True
    """
    return _finder(_SYMB_SET, tag)


def is_unknown(tag) -> bool:
    """
    주어진 품사표기/형태소가 분석되지 않은 미상의 형태소인지 확인합니다.

    :param Union[str,Morpheme] tag: 확인할 품사 또는 형태소.
    :return bool: 미상의 형태소이면 True
    """
    return _finder(_UNKN_SET, tag)
