#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class API(Enum):
    """ 지원하는 분석기의 종류. """
    HANNANUM = 'hnn'     #: 한나눔
    KOMORAN = 'kmr'      #: 코모란
    KKMA = 'kkma'        #: 꼬꼬마
    EUNJEON = 'eunjeon'  #: 은전한닢
    ARIRANG = 'arirang'  #: 아리랑
    RHINO = 'rhino'      #: 라이노
    TWITTER = 'twt'      #: 트위터

def _artifactName(api):
    if api == API.HANNANUM:
        return 'hannanum'
    elif api == API.KOMORAN:
        return 'komoran'
    elif api == API.KKMA:
        return 'kkma'
    elif api == API.EUNJEON:
        return 'eunjeon'
    elif api == API.ARIRANG:
        return 'arirang'
    elif api == API.RHINO:
        return 'rhino'
    elif api == API.TWITTER:
        return 'twitter'
    else:
        return 'core'