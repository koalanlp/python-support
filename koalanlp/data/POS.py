from ._data import Morpheme

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


def _finder(sets, tag):
    if type(tag) is str:
        return sets.index(tag) >= 0
    elif type(tag) is Morpheme:
        return sets.index(tag.tag) >= 0
    else:
        return False


def is_noun(tag):
    return _finder(_NOUN_SET, tag)


def is_predicate(tag):
    return _finder(_PRED_SET, tag)


def is_modifier(tag):
    return _finder(_MODF_SET, tag)


def is_postposition(tag):
    return _finder(_JOSA_SET, tag)


def is_ending(tag):
    return _finder(_EOMI_SET, tag)


def is_affix(tag):
    return _finder(_AFFX_SET, tag)


def is_suffix(tag):
    return _finder(_SUFX_SET, tag)


def is_symbol(tag):
    return _finder(_SYMB_SET, tag)


def is_unknown(tag):
    return _finder(_UNKN_SET, tag)
