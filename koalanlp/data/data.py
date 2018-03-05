#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import POS


class Morpheme(object):
    """ 형태소 객체. """

    surface = ""    #: 형태소의 표면형
    tag = ""        #: 세종 품사
    raw_tag = ""    #: 품사 분석기의 원본결과인 품사
    index = -1      #: 어절 내 위치

    def __init__(self, surface: str, tag: str, raw_tag: str, index: int):
        """
        형태소 객체를 생성합니다.

        :param str surface: 형태소의 표면형.
        :param str tag: 세종 품사
        :param str raw_tag: 품사분석기의 원본 분석결과인 품사.
        :param int index: 어절 내 위치
        """
        assert type(surface) is str
        assert type(tag) is str
        assert type(raw_tag) is str
        assert type(index) is int
        self.surface = surface
        self.tag = tag
        self.raw_tag = raw_tag
        self.index = index

    def has_tag(self, tag) -> bool:
        """
        주어진 형태소와 일치하는지 확인합니다.

        :param Union[list[str],str] tag: 일치하는지 확인할 품사 또는 품사의 목록.
        :return: 하나라도 일치하면 True.
        """
        if type(tag) is str:
            return self.tag.startswith(tag)
        elif type(tag) is list:
            for v in tag:
                if self.tag.startswith(v):
                    return True
            else:
                return False
        else:
            return False

    def has_raw_tag(self, tag) -> bool:
        """
        주어진 형태소와 원본품사가 일치하는지 확인합니다.

        :param Union[list[str],str] tag: 일치하는지 확인할 품사 또는 품사의 목록.
        :return: 하나라도 일치하면 True.
        """
        if type(tag) is str:
            return self.raw_tag.startswith(tag)
        elif type(tag) is list:
            for v in tag:
                if self.raw_tag.startswith(v):
                    return True
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        """
        주어진 형태소와 표면형 및 품사가 일치하는지 확인합니다.

        :param other: 비교할 형태소
        :return: 일치하면, True
        """
        if type(other) is Morpheme:
            return other.surface == self.surface and other.tag == self.tag
        else:
            return False

    def equals_without_tag(self, morph):
        """
        주어진 형태소와 표면형이 일치하는지 확인합니다.

        :param morph: 비교할 형태소
        :return: 일치하면, True
        """
        if type(morph) is Morpheme:
            return morph.surface == self.surface
        else:
            return False

    def __repr__(self):
        return "%s/%s(%s)" % (self.surface, self.tag, self.raw_tag)

    def to_dict(self) -> dict:
        """
        형태소를 dict 객체로 변환합니다.

        :return dict: 표면형, 품사, 원본품사, 위치를 담은 dict.
        """
        return {
            "surface": self.surface,
            "tag": self.tag,
            "rawTag": self.tag,
            "id": self.index
        }


class Relationship(object):
    """ 의존관계 객체. """

    head = -1       #: 지배소의 문장 내 위치
    relation = ""   #: 의존관계
    raw_rel = ""    #: 의존구문분석기가 도출한 원본 의존관계
    target = -1     #: 피지배소(의존소)의 문장 내 위치

    def __init__(self, head: int, relation: str, raw_rel: str, target: int):
        """
        의존관계 객체를 생성합니다.

        :param int head: 지배소의 문장 내 위치
        :param str relation: 의존관계
        :param str raw_rel: 의존구문분석기가 도출한 원본 의존관계.
        :param int target: 피지배소(의존소)의 문장 내 위치
        """
        assert type(head) is int
        assert type(relation) is str
        assert type(raw_rel) is str
        assert type(target) is int

        self.head = head
        self.relation = relation
        self.raw_rel = raw_rel
        self.target = target

    def __eq__(self, other):
        """
        주어진 관계와 지배소, 피지배소, 관계가 일치하는지 확인합니다.

        :param other: 비교할 의존관계
        :return: 일치하면, True
        """
        if type(other) is Relationship:
            return self.head == other.head and self.relation == other.relation and self.target == other.target
        else:
            return False

    def __repr__(self):
        return "Rel:%s (ID:%s → ID:%s)" % (self.relation, self.head, self.target)

    def to_dict(self) -> dict:
        """
        의존관계를 dict 객체로 변환합니다.

        :return dict: 지배소, 피지배소, 관계, 원본관계를 담은 dict.
        """
        return {
            "head_id": self.head,
            "target_id": self.target,
            "relation": self.relation,
            "raw_rel": self.raw_rel
        }


class Word(object):
    """ 어절 객체 """

    surface = "##ROOT##"    #: 어절의 표면형.
    morphemes = []          #: 어절에 포함된 형태소 목록.
    index = -1              #: 어절의 문장 내 위치.
    dependents = []         #: 어절에 의존하는 의존관계 목록.

    def __init__(self, surface: str=None, morphemes=None, index: int=None):
        """
        어절 객체를 생성합니다.

        :param str surface: 어절의 표면형.
        :param list[Morpheme] morphemes: 어절에 포함된 형태소 목록.
        :param int index: 어절의 문장 내 위치.
        """
        if surface is not None:
            assert type(surface) is str
            assert type(morphemes) is list, type(morphemes[0]) is Morpheme
            assert type(index) is int

            self.surface = surface
            self.morphemes = morphemes
            self.index = index
        self.dependents = []

    def __len__(self) -> int:
        """
        어절 속 형태소 개수

        :return int: 형태소 개수
        """
        return len(self.morphemes)

    def __getitem__(self, item: int) -> Morpheme:
        """
        주어진 위치의 형태소를 반환합니다.

        :param int item: 형태소를 찾을 위치.
        :return Morpheme: 찾은 형태소.
        """
        return self.morphemes[item]

    def __iter__(self):
        """
        어절 내 형태소의 iterator

        :return: 형태소 iterator
        """
        return iter(self.morphemes)

    def matches(self, tag) -> bool:
        """
        어절 내 형태소의 순서가 주어진 순서와 일치하는지 확인합니다.

        :param list[str] tag: 확인할 품사의 순서.
        :return bool: 순서가 일치하면, True (연속할 필요는 없음)
        """
        if type(tag) is list:
            tag_list = tag.copy()
            for m in self.morphemes:
                if len(tag_list) > 0 and m.tag.startswith(tag_list[0]):
                    del tag_list[0]
            return len(tag_list) == 0
        else:
            return False

    def find(self, fn):
        """
        주어진 형태소/조건에 일치하는 형태소를 찾습니다.

        :param Union[Morpheme,function[Morpheme,bool]] fn: 찾을 형태소/조건.
        :return Morpheme: 일치하는 형태소.
        """
        if callable(fn):
            for m in self.morphemes:
                if fn(m):
                    return m
            else:
                return None
        elif type(fn) is Morpheme:
            for m in self.morphemes:
                if m == fn:
                    return m
            else:
                return None
        else:
            return None

    def __contains__(self, item) -> bool:
        """
        주어진 형태소/조건에 일치하는 형태소가 있는지 확인합니다.

        :param Union[Morpheme,function[Morpheme,bool]] item: 찾을 형태소/조건.
        :return bool: 일치하는 형태소가 있다면, True
        """
        return not(self.find(item) is None)

    def exists(self, fn) -> bool:
        """
        주어진 형태소/조건에 일치하는 형태소가 있는지 확인합니다.

        :param Union[Morpheme,function[Morpheme,bool]] fn: 찾을 형태소/조건.
        :return bool: 일치하는 형태소가 있다면, True
        """
        return self.__contains__(fn)

    def equals_without_tag(self, another) -> bool:
        """
        두 어절이 표면형이 일치하는지 확인합니다.

        :param another: 비교할 어절
        :return bool: 표면형이 일치하면, True
        """
        if type(another) is Word:
            return another.surface == self.surface
        else:
            return False

    def __eq__(self, other) -> bool:
        """
        두 어절이 표면형, 위치가 일치하는지 확인합니다.

        :param other: 비교할 어절
        :return bool: 표면형과 위치가 일치하면, True
        """
        if type(other) is Word:
            is_equal = other.index == self.index and len(self) == len(other)
            for i in range(len(self)):
                is_equal = is_equal and self[i] == other[i]
            return is_equal
        else:
            return False

    def __repr__(self):
        morph_str = "+".join([str(m) for m in self.morphemes])
        repr_str = "%s\t= %s" % (self.surface, morph_str)
        if len(self.dependents) > 0:
            for r in self.dependents:
                repr_str += "\n.... 이 어절의 %s: 어절 [#%s]" % (r.relation, r.target)
        return repr_str

    def single_line_string(self) -> str:
        """
        형태소 분석 결과를 한 행에 표현합니다.

        :return str: "형태소1/품사1+형태소2/품사2..." 형태의 문자열.
        """
        repr_str = ["%s/%s" % (m.surface, m.tag) for m in self.morphemes]
        return "+".join(repr_str)

    def to_dict(self) -> dict:
        """
        어절을 dict 객체로, 변환합니다.

        :return dict: 표면형, 형태소, 의존관계, 위치를 담은 dict
        """
        return {
            "surface": self.surface,
            "morphemes": [m.to_dict() for m in self.morphemes],
            "dependents": [r.to_dict() for r in self.dependents],
            "id": self.index
        }


class Sentence(object):
    """ 문장 객체. """

    words = []          #: 문장을 구성하는 어절의 목록.
    root = None         #: 문장의 핵심어(최상위 지배소)의 목록.
    reference = None    #: KoalaNLP(Java)가 분석한 결과.

    def __init__(self, words, reference):
        """
        문장 객체를 생성합니다.

        :param list[Word] words: 문장을 구성하는 어절의 목록.
        :param reference: KoalaNLP(Java)가 분석한 결과.
        """
        assert type(words) is list, type(words[0]) is Word
        self.words = words
        self.root = Word()
        self.reference = reference

    def matches(self, tag) -> bool:
        """
        문장 내 형태소의 순서가 주어진 순서와 일치하는지 확인합니다.

        :param list[list[str]] tag: 확인할 품사의 순서. 품사의 묶음(어절)의 묶음
        :return bool: 순서가 일치하면, True (연속할 필요는 없음)
        """
        if type(tag) is list:
            tag_list = tag.copy()
            for w in self.words:
                if len(tag_list) > 0 and w.matches(tag_list[0]):
                    del tag_list[0]
            return len(tag_list) == 0
        else:
            return False

    def find(self, fn):
        """
        주어진 어절/조건에 일치하는 어절을 찾습니다.

        :param Union[Word,function[Word,bool]] fn: 찾을 어절/조건.
        :return Word: 일치하는 어절.
        """
        if callable(fn):
            for m in self.words:
                if fn(m):
                    return m
            else:
                return None
        elif type(fn) is Word:
            for m in self.words:
                if m == fn:
                    return m
            else:
                return None
        else:
            return None

    def __contains__(self, item) -> bool:
        """
        주어진 어절/조건에 일치하는 어절이 있는지 확인합니다.

        :param Union[Word,function[Word,bool]] item: 찾을 어절/조건.
        :return bool: 일치하는 어절이 있다면, True
        """
        return not(self.find(item) is None)

    def exists(self, fn) -> bool:
        """
        주어진 어절/조건에 일치하는 어절이 있는지 확인합니다.

        :param Union[Word,function[Word,bool]] fn: 찾을 어절/조건.
        :return bool: 일치하는 어절이 있다면, True
        """
        return self.__contains__(fn)

    def nouns(self):
        """
        문장 내 체언(명사,대명사,의존명사,수사)을 포함한 어절의 목록.

        :return list[word]: 체언 어절 목록
        """
        return [w for w in self.words if w.exists(POS.is_noun)]

    def verbs(self):
        """
        문장 내 용언(동사,형용사)을 포함한 어절의 목록.

        :return list[word]: 용언 어절 목록
        """
        return [w for w in self.words if w.exists(POS.is_predicate)]

    def modifiers(self):
        """
        문장 내 수식언(관형사,부사)을 포함한 어절의 목록.

        :return list[word]: 수식언 어절 목록
        """
        return [w for w in self.words if w.exists(POS.is_modifier)]

    def __getitem__(self, item: int) -> Word:
        """
        주어진 위치의 어절을 반환합니다.

        :param int item: 어절을 찾을 위치.
        :return Word: 찾은 어절.
        """
        return self.words[item]

    def __len__(self) -> int:
        """
        문장 속 어절의 수

        :return int: 어절의 수.
        """
        return len(self.words)

    def __iter__(self):
        """
        문장 속 어절을 순회하는 iterator

        :return: 어절 순회 iterator
        """
        return iter(self.words)

    def __repr__(self):
        repr_str = self.surface_string() + "\n"
        for w in self.words:
            repr_str += "[#%s] %s" % (w.index, str(w))
            is_root = len([r for r in self.root.dependents if r.target == w.index])
            if is_root > 0:
                repr_str += "\n.... 이 어절이 ROOT 입니다"
            repr_str += "\n"
        return repr_str

    def surface_string(self, delimiter: str=" ") -> str:
        """
        문장의 표면형을 모아 한 행으로 만듭니다.

        :param str delimiter: 어절을 구분할 구분자. (기본 = Space)
        :return str: delimiter로 구분된 문장의 표면형.
        """
        return delimiter.join([w.surface for w in self.words])

    def single_line_string(self) -> str:
        """
        문장의 품사 분석 결과를 한 행으로 만듭니다.

        :return str: "형태소1/품사1+형태소2/품사2..."로 표현된 어절을 빈칸으로 구분한 한 행짜리 문자열.
        """
        return " ".join([w.single_line_string() for w in self.words])

    def to_dict(self) -> dict:
        """
        문장을 dict로 변환.

        :return dict: 어절과 최상위 의존관계를 포함한 dict.
        """
        return {
            "words": [m.to_dict() for m in self.words],
            "root": [r.to_dict() for r in self.root.dependents]
        }
