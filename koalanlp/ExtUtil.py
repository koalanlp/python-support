#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, Dict, List

from .jnius import *


def ChoToJong() -> Dict[str, str]:
    """
    :rtype: Dict[str, str]
    :return: 초성 문자를 종성 조합형 문자로 변경
    """
    return py_dict(koala_class_of('ExtUtil').ChoToJong, py_str, py_str)


def HanFirstList() -> List[str]:
    """
    :rtype: List[str]
    :return: 초성 조합형 문자열 리스트 (UNICODE 순서)
    """
    return py_list(koala_class_of('ExtUtil').HanFirstList, py_str)


def HanSecondList() -> List[str]:
    """
    :rtype: List[str]
    :return: 중성 조합형 문자열 리스트 (UNICODE 순서)
    """
    return py_list(koala_class_of('ExtUtil').HanSecondList, py_str)


def HanLastList() -> List[str]:
    """
    :rtype: List[str]
    :return: 종성 조합형 문자열 리스트 (UNICODE 순서). 가장 첫번째는 null (받침 없음)
    """
    return py_list(koala_class_of('ExtUtil').HanLastList, py_str)


def alphaToHangul(text: str) -> str:
    """
    주어진 문자열에서 알파벳이 발음되는 대로 국문 문자열로 표기하여 값으로 돌려줍니다.

    :param str text: 알파벳을 발음할 문자열
    :rtype: str
    :return: 국문 발음 표기된 문자열
    """

    return koala_class_of('ExtUtil').alphaToHangul(string(text))


def hangulToAlpha(text: str) -> str:
    """
    주어진 문자열에 적힌 알파벳 발음을 알파벳으로 변환하여 문자열로 반환합니다.

    :param str text: 국문 발음 표기된 문자열
    :rtype: str
    :return: 영문 변환된 문자열
    """

    return koala_class_of('ExtUtil').hangulToAlpha(string(text))


def isAlphaPronounced(text: str) -> bool:
    """
    주어진 문자열이 알파벳이 발음되는 대로 표기된 문자열인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: bool
    :return: 영문 발음으로만 구성되었다면 true
    """

    return koala_class_of('ExtUtil').isAlphaPronounced(string(text))


def isHanja(text: str) -> List[bool]:
    """
    문자열의 각 문자가 한자 범위인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 한자인지 아닌지를 표기한 리스트. 한자라면 True.
    """

    return [koala_class_of('ExtUtil').isHanja(char(ch)) for ch in text]


def isCJKHanja(text: str) -> List[bool]:
    """
    현재 문자가 한중일 통합한자, 통합한자 확장 - A, 호환용 한자 범위인지 확인합니다.
    (국사편찬위원회 한자음가사전은 해당 범위에서만 정의되어 있어, 별도 확인합니다.)

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 한자인지 아닌지를 표기한 리스트. 한자라면 True.
    """

    return [koala_class_of('ExtUtil').isCJKHanja(char(ch)) for ch in text]


def hanjaToHangul(text: str, headCorrection: bool=True) -> str:
    """
    국사편찬위원회 한자음가사전에 따라 한자 표기된 내용을 국문 표기로 전환합니다.

    참고:

        * [headCorrection] 값이 true인 경우, whitespace에 따라오는 문자에 두음법칙을 자동 적용함. (기본값 true)
        * 단, 다음 의존명사는 예외: 냥(兩), 년(年), 리(里), 리(理), 량(輛)
        * 다음 두음법칙은 사전을 조회하지 않기 때문에 적용되지 않음에 유의
            - 한자 파생어나 합성어에서 원 단어의 두음법칙: 예) "신여성"이 옳은 표기이나 "신녀성"으로 표기됨
            - 외자가 아닌 이름: 예) "허난설헌"이 옳은 표기이나 "허란설헌"으로 표기됨

    :param text: 국문 표기로 전환할 문자열
    :param headCorrection: 두음법칙 적용 여부 (기본값 True)
    :return: 국문 표기로 전환된 문자열
    """

    return koala_class_of('ExtUtil').hanjaToHangul(string(text), headCorrection)


def isCompleteHangul(text: str) -> List[bool]:
    """
    현재 문자가 초성, 중성, 종성(선택적)을 다 갖춘 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isCompleteHangul(char(ch)) for ch in text]


def isIncompleteHangul(text: str) -> List[bool]:
    """
    현재 문자가 불완전한 한글 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isIncompleteHangul(char(ch)) for ch in text]


def isHangul(text: str) -> List[bool]:
    """
    현재 문자가 한글 완성형 또는 조합용 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isHangul(char(ch)) for ch in text]


def isHangulEnding(text: str) -> bool:
    """
    현재 문자열이 한글 (완성/조합)로 끝나는지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: bool
    :return: 맞다면 True.
    """

    return koala_class_of('ExtUtil').isHangulEnding(string(text))


def isChosungJamo(text: str) -> List[bool]:
    """
    현재 문자가 현대 한글 초성 자음 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isChosungJamo(char(ch)) for ch in text]


def isJungsungJamo(text: str) -> List[bool]:
    """
    현재 문자가 현대 한글 중성 모음 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isJungsungJamo(char(ch)) for ch in text]


def isJongsungJamo(text: str) -> List[bool]:
    """
    현재 문자가 현대 한글 종성 자음 문자인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: List[bool]
    :return: 문자열 문자의 위치마다 확인여부를 표기한 리스트. 맞다면 True.
    """

    return [koala_class_of('ExtUtil').isJongsungJamo(char(ch)) for ch in text]


def isJongsungEnding(text: str) -> bool:
    """
    현재 문자열이 종성으로 끝인지 확인합니다.

    :param str text: 확인할 문자열
    :rtype: bool
    :return: 맞다면 True.
    """

    return koala_class_of('ExtUtil').isJongsungEnding(string(text))


def getChosung(text: str) -> List[Union[None, str]]:
    """
    현재 문자에서 초성 자음문자를 분리합니다. 초성이 없으면 None.

    :param str text: 분리할 문자열
    :rtype: List[Union[None,str]]
    :return: 분리된 각 초성이 들어간 리스트.
    """

    return [koala_class_of('ExtUtil').getChosung(char(ch)) for ch in text]


def getJungsung(text: str) -> List[Union[None, str]]:
    """
    현재 문자에서 중성 모음문자를 분리합니다. 중성이 없으면 None.

    :param str text: 분리할 문자열
    :rtype: List[Union[None,str]]
    :return: 분리된 각 중성이 들어간 리스트.
    """

    return [koala_class_of('ExtUtil').getJungsung(char(ch)) for ch in text]


def getJongsung(text: str) -> List[Union[None, str]]:
    """
    현재 문자에서 종성 자음문자를 분리합니다. 종성이 없으면 None.

    :param str text: 분리할 문자열
    :rtype: List[Union[None,str]]
    :return: 분리된 각 종성이 들어간 리스트.
    """

    return [koala_class_of('ExtUtil').getJongsung(char(ch)) for ch in text]


def dissembleHangul(text: str) -> str:
    """
    현재 문자열을 초성, 중성, 종성 자음문자로 분리하여 새 문자열을 만듭니다. 종성이 없으면 종성은 쓰지 않습니다.

    :param str text: 분해할 문자열
    :rtype: str
    :return: 분해된 문자열
    """

    return koala_class_of('ExtUtil').dissembleHangul(string(text))


def assembleHangulTriple(cho: Union[str, None] = None, jung: Union[str, None] = None,
                         jong: Union[str, None] = None) -> str:
    """
    초성을 [cho] 문자로, 중성을 [jung] 문자로, 종성을 [jong] 문자로 갖는 한글 문자를 재구성합니다.

    :param str cho: 초성 문자. (0x1100-1112) 기본값 ㅇ 자모
    :param str jung: 중성 문자, (0x1161-1175) 기본값 ㅡ 자모
    :param str jong: 종성 문자, (0x11a8-11c2) 기본값 종성 없음
    :rtype: str
    :return: 초성, 중성, 종성을 조합하여 문자를 만듭니다.
    """

    return koala_class_of('ExtUtil').assembleHangul(char(cho), char(jung), char(jong))


def assembleHangul(text: str) -> str:
    """
    주어진 문자열에서 초성, 중성, 종성이 연달아 나오는 경우 이를 조합하여 한글 문자를 재구성합니다.

    :param str text: 조합할 문자열
    :rtype: str
    :return: 조합형 문자들이 조합된 문자열. 조합이 불가능한 문자는 그대로 남습니다.
    """

    return koala_class_of('ExtUtil').assembleHangul(string(text))


def correctVerbApply(verb: str, isVerb: bool, rest: str) -> str:
    """
    주어진 용언의 원형 [verb]이 뒷 부분 [rest]와 같이 어미가 붙어 활용될 때, 불규칙 활용 용언과 모음조화를 교정합니다.

    :param str verb: 용언 원형인 어근을 표현한 String. '-다.' 와 같은 어미는 없는 어근 상태입니다.
    :param bool isVerb: 동사인지 형용사인지 나타내는 지시자. 동사이면 true.
    :param str rest: 어근에 붙일 어미를 표현한 String.
    :rtype: str
    :return: 모음조화나 불규칙 활용이 교정된 원형+어미 결합
    """

    return koala_class_of('ExtUtil').correctVerbApply(string(verb), isVerb, string(rest))


# ----- Define members exported -----

__all__ = [
    'ChoToJong',
    'HanFirstList',
    'HanSecondList',
    'HanLastList',
    'alphaToHangul',
    'hangulToAlpha',
    'isAlphaPronounced',
    'isHanja',
    'isCJKHanja',
    'hanjaToHangul',
    'isCompleteHangul',
    'isIncompleteHangul',
    'isHangul',
    'isHangulEnding',
    'isChosungJamo',
    'isJungsungJamo',
    'isJongsungJamo',
    'isJongsungEnding',
    'getChosung',
    'getJungsung',
    'getJongsung',
    'dissembleHangul',
    'assembleHangulTriple',
    'assembleHangul',
    'correctVerbApply'
]