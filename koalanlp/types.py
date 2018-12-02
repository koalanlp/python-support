#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .jnius import *


def _enum_value_dict(cls, item_converter):
    return {value.name: value for value in py_list(koala_class_of(cls).values(), item_converter)}


class _JavaEnum(object):
    name = ''  #: Enum 명칭
    ordinal = -1  #: 순서 번호

    def __init__(self, reference):
        self.name = reference.name()
        self.ordinal = reference.ordinal()
        self.classType = reference.getClass().getName()

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, _JavaEnum) and other.classType == self.classType and other.ordinal == self.ordinal


class POS(_JavaEnum):
    """ 세종 품사표기 """

    __VALUES__ = {}

    def __init__(self, reference):
        """
        세종 품사표기 표준안을 Enum Class로 담았습니다.
        """
        self.reference = reference
        super().__init__(self.reference)

    @staticmethod
    def values():
        """
        POS 값들을 모두 돌려줍니다.

        :rtype: Set[POS]
        :return: 모든 품사 태그의 Set
        """
        if len(POS.__VALUES__) == 0:
            POS.__VALUES__ = _enum_value_dict(__class__.__name__, lambda x: POS(x))
            for name, value in POS.__VALUES__.items():
                setattr(POS, name, value)

        return POS.__VALUES__.values()

    @staticmethod
    def valueOf(name: str):
        """
        해당하는 name과 일치하는 POS 값을 돌려줍니다.

        :param str name: POS 값을 찾을 명칭.

        :rtype: POS
        :return: 일치하는 POS값
        """
        return getattr(POS, name)

    def isNoun(self) -> bool:
        """
        이 값이 체언인지 확인합니다.

        :rtype: bool
        :return: 체언인 경우 True
        """
        return self.reference.isNoun()

    def isPredicate(self) -> bool:
        """
        이 값이 용언인지 확인합니다.

        :rtype: bool
        :return: 용언인 경우 True
        """
        return self.reference.isPredicate()

    def isModifier(self) -> bool:
        """
        이 값이 수식언인지 확인합니다.

        :rtype: bool
        :return: 수식언인 경우 True
        """
        return self.reference.isModifier()

    def isPostPosition(self) -> bool:
        """
        이 값이 관계언(조사)인지 확인합니다.

        :rtype: bool
        :return: 관계언인 경우 True
        """
        return self.reference.isPostPosition()

    def isEnding(self) -> bool:
        """
        이 값이 어미인지 확인합니다.

        :rtype: bool
        :return: 어미인 경우 True
        """
        return self.reference.isEnding()

    def isAffix(self) -> bool:
        """
        이 값이 접사인지 확인합니다.

        :rtype: bool
        :return: 접사인 경우 True
        """
        return self.reference.isAffix()

    def isSuffix(self) -> bool:
        """
        이 값이 접미사인지 확인합니다.

        :rtype: bool
        :return: 접미사인 경우 True
        """
        return self.reference.isSuffix()

    def isSymbol(self) -> bool:
        """
        이 값이 기호인지 확인합니다.

        :rtype: bool
        :return: 기호인 경우 True
        """
        return self.reference.isSymbol()

    def isUnknown(self) -> bool:
        """
        이 값이 미확인 단어인지 확인합니다.

        :rtype: bool
        :return: 미확인 단어인 경우 True
        """
        return self.reference.isUnknown()

    def startsWith(self, tag: str) -> bool:
        """
        이 값이 주어진 [tag]로 시작하는지 확인합니다.

        :param str tag: 시작하는지 확인할 품사 분류

        :return: 포함되는 경우(시작하는 경우) True
        """
        return self.reference.startsWith(string(tag))


class PhraseTag(_JavaEnum):
    """ 세종 구문구조 표지자 """

    __VALUES__ = {}

    @staticmethod
    def values():
        """
        PhraseTag 값들을 모두 돌려줍니다.

        :rtype: Set[PhraseTag]
        :return: 모든 구문구조 태그의 Set
        """
        if len(PhraseTag.__VALUES__) == 0:
            PhraseTag.__VALUES__ = _enum_value_dict(__class__.__name__, lambda x: PhraseTag(x))
            for name, value in PhraseTag.__VALUES__.items():
                setattr(PhraseTag, name, value)

        return PhraseTag.__VALUES__.values()

    @staticmethod
    def valueOf(name: str):
        """
        해당하는 name과 일치하는 PhraseTag 값을 돌려줍니다.

        :param str name: 값을 찾을 명칭.

        :rtype: PhraseTag
        :return: 일치하는 PhraseTag값
        """
        return getattr(PhraseTag, name)


class DependencyTag(_JavaEnum):
    """ ETRI 의존구문구조 기능표지자 """

    __VALUES__ = {}

    @staticmethod
    def values():
        """
        DependencyTag 값들을 모두 돌려줍니다.

        :rtype: Set[DependencyTag]
        :return: 모든 의존구조 기능 태그의 Set
        """
        if len(DependencyTag.__VALUES__) == 0:
            DependencyTag.__VALUES__ = _enum_value_dict(__class__.__name__, lambda x: DependencyTag(x))
            for name, value in DependencyTag.__VALUES__.items():
                setattr(DependencyTag, name, value)

        return DependencyTag.__VALUES__.values()

    @staticmethod
    def valueOf(name: str):
        """
        해당하는 name과 일치하는 DependencyTag 값을 돌려줍니다.

        :param str name: 값을 찾을 명칭.

        :rtype: DependencyTag
        :return: 일치하는 DependencyTag값
        """
        return getattr(DependencyTag, name)


class RoleType(_JavaEnum):
    """ ETRI 의미역 분석 표지 """

    __VALUES__ = {}

    @staticmethod
    def values():
        """
        RoleType 값들을 모두 돌려줍니다.

        :rtype: Set[RoleType]
        :return: 모든 의미역 태그의 Set
        """

        if len(RoleType.__VALUES__) == 0:
            RoleType.__VALUES__ = _enum_value_dict(__class__.__name__, lambda x: RoleType(x))
            for name, value in RoleType.__VALUES__.items():
                setattr(RoleType, name, value)

        return RoleType.__VALUES__.values()

    @staticmethod
    def valueOf(name: str):
        """
        해당하는 name과 일치하는 RoleType 값을 돌려줍니다.

        :param str name: 값을 찾을 명칭.

        :rtype: RoleType
        :return: 일치하는 RoleType값
        """
        return getattr(RoleType, name)


class CoarseEntityType(_JavaEnum):
    """ ETRI 개체명 대분류 """
    __VALUES__ = {}

    @staticmethod
    def values():
        """
        CoarseEntityType 값들을 모두 돌려줍니다.

        :rtype: Set[CoarseEntityType]
        :return: 모든 개체명 태그의 Set
        """
        if len(CoarseEntityType.__VALUES__) == 0:
            CoarseEntityType.__VALUES__ = _enum_value_dict(__class__.__name__, lambda x: CoarseEntityType(x))
            for name, value in CoarseEntityType.__VALUES__.items():
                setattr(CoarseEntityType, name, value)

        return CoarseEntityType.__VALUES__.values()

    @staticmethod
    def valueOf(name: str):
        """
        해당하는 name과 일치하는 CoarseEntityType 값을 돌려줍니다.

        :param str name: 값을 찾을 명칭.

        :rtype: CoarseEntityType
        :return: 일치하는 CoarseEntityType값
        """
        return getattr(CoarseEntityType, name)


# ----- Declare members exported -----

__all__ = ['POS', 'CoarseEntityType', 'PhraseTag', 'DependencyTag', 'RoleType']
