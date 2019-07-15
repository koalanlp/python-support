#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .jvm import *

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
    api = api.lower()

    if not is_jvm_running():
        raise Exception("사용 전 초기화 과정이 필요합니다. 사용법의 Util.initialize 문서를 참고하여 초기화를 해주세요."
                        "사용하신 코드를 토대로는 다음 코드의 실행을 추천해드립니다.\n"
                        "from koalanlp.Util import initialize"
                        "initialize(%s='LATEST')" % api)

    try:
        java_api = koala_class_of(api, type)
        return java_api
    except Exception:
        raise Exception('API.%s는 %s를 지원하지 않는 것 같습니다.'
                        'API 문서에서 지원여부를 다시 한번 확인해주시고, 지원한다고 적혀있어도 혹시 문제가 지속된다면 이슈를 올려주세요.' %
                        (api.upper(), str(type)))


# ----- Define members exported -----

__all__ = ['HNN', 'KMR', 'KKMA', 'EUNJEON', 'ARIRANG', 'RHINO', 'OKT', 'DAON', 'ETRI', 'CORE']
