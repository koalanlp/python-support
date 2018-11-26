#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .jnius import *

HNN = 'hnn'          #: 한나눔. 현재 |ver_hnn| 버전이 최신입니다. 문장분리, 품사분석, 구문분석, 의존분석이 가능합니다.
KMR = 'kmr'          #: 코모란. 현재 |ver_kmr| 버전이 최신입니다. 품사분석만 가능합니다.
KKMA = 'kkma'        #: 꼬꼬마. 현재 |ver_kkma| 버전이 최신입니다. 품사분석, 의존분석만 가능합니다.
EUNJEON = 'eunjeon'  #: 은전한닢. 현재 |ver_eunjeon| 버전이 최신입니다. 품사분석만 가능합니다.
ARIRANG = 'arirang'  #: 아리랑. 현재 |ver_arirang| 버전이 최신입니다. 품사분석만 가능합니다.
RHINO = 'rhino'      #: 라이노. 현재 |ver_rhino| 버전이 최신입니다. 품사분석만 가능합니다.
OKT = 'okt'          #: 트위터. 현재 |ver_okt| 버전이 최신입니다. 문장분리, 품사분석만 가능합니다.
DAON = 'daon'        #: 다온. 현재 |ver_daon| 버전이 최신입니다. 품사분석만 가능합니다.
ETRI = 'etri'        #: ETRI Open API. 현재 |ver_etri| 버전이 최신입니다.
CORE = 'core'        #: 분석기 Interface 정의 라이브러리. 현재 |ver_core| 버전이 최신입니다. 편의기능을 제공하며 타 분석기 참조시 함께 참조됩니다.

_REQUIRE_ASSEMBLY_ = [HNN, KKMA, ARIRANG, RHINO, DAON]   #: 'assembly' classifier 필요 여부


def _query(api: str, type: str):
    try:
        java_api = koala_class_of(api, type)
        return java_api
    except Exception:
        raise Exception('API.%s는 %s를 지원하지 않습니다!' % (api.upper(), str(type)))


# ----- Define members exported -----

__all__ = ['HNN', 'KMR', 'KKMA', 'EUNJEON', 'ARIRANG', 'RHINO', 'OKT', 'DAON', 'ETRI', 'CORE']
