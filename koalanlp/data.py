#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .types import *
from .jnius import *
from typing import List, Optional


class _PyListWrap(object):
    _ref_list = None

    def __setattr__(self, name, value):
        if name not in ['_ref_list']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def __init__(self, ref_list):
        self._ref_list = ref_list

    def __getitem__(self, item):
        """
        포함된 대상을 가져옵니다.

        :param item: index의 번호 또는 slice
        :return: 지정된 위치에 있는 대상(들)
        """
        return self._ref_list[item]

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 대상을 순회하는 iterator
        """
        return iter(self._ref_list)

    def __contains__(self, item) -> bool:
        """
        대상이 포함되는지 확인합니다.

        :param item: 포함되는지 확인할 대상
        :rtype: bool
        :return: 해당 대상이 포함되면 true.
        """
        return item in self._ref_list

    def __len__(self):
        """
        :rtype: int
        :return: 포함된 대상의 개수
        """
        return len(self._ref_list)

    def __eq__(self, other) -> bool:
        """
        두 대상이 같은지 확인합니다.

        :param other: 이 객체와 비교할 다른 객체
        :rtype: bool
        :return: Java Reference가 같다면 true.
        """
        return type(other) is type(self) and len(self) == len(other) and all(x == y for x, y in zip(self, other))

    def __hash__(self) -> int:
        """
        해쉬 값을 계산합니다.

        :rtype: int
        :return: Java Reference의 Hash code
        """
        return sum(hash(x) for x in self)


class Entity(_PyListWrap):
    """
    개체명 분석 결과를 저장할 [Property] class

    참고:
        **개체명 인식** 은 문장에서 인물, 장소, 기관, 대상 등을 인식하는 기술입니다.

        예) '철저한 진상 조사를 촉구하는 국제사회의 목소리가 커지고 있는 가운데, 트럼프 미국 대통령은 되레 사우디를 감싸고 나섰습니다.'에서, 다음을 인식하는 기술입니다.

        * '트럼프': 인물
        * '미국' : 국가
        * '대통령' : 직위
        * '사우디' : 국가

        아래를 참고해보세요.

        * :py:class:`koalanlp.proc.EntityRecognizer` 개체명 인식기 interface
        * :py:meth:`koalanlp.data.Morpheme.getEntities` 형태소가 속하는 [Entity]를 가져오는 API
        * :py:meth:`koalanlp.data.Word.getEntities` 어절에 연관된 모든 [Entity]를 가져오는 API
        * :py:meth:`koalanlp.data.Sentence.getEntities` 문장에 포함된 모든 [Entity]를 가져오는 API
        * :py:class:`koalanlp.types.CoarseEntityType` [Entity]의 대분류 개체명 분류구조 Enum 값
    """
    corefGroup = None  #: 공지시어 해소 또는 대용어 분석 결과. :py:meth:`getCorefGroup` 참고.
    surface = None  #: 개체명 표면형.
    label = None  #: 개체명 대분류 값
    fineLabel = None  #: 개체명 세분류 값
    originalLabel = None  #: 원본 분석기가 제시한 개체명 분류의 값.

    def __init__(self, surface: str, label: str, fineLabel: str, morphemes: List, originalLabel: str = None):
        """
        개체명 분석 결과를 저장합니다.
        :param str surface: 개체명의 표면형 문자열.
        :param str label: 개체명 대분류 값, [CoarseEntityType]에 기록된 개체명 중 하나.
        :param str fineLabel: 개체명 세분류 값으로, [label]으로 시작하는 문자열.
        :param List[Morpheme] morphemes: 개체명을 이루는 형태소의 목록
        :param str originalLabel: 원본 분석기가 제시한 개체명 분류의 값. 기본값은 None.
        """
        assert surface is not None and label is not None and fineLabel is not None and morphemes is not None, \
            "[surface, label, fineLabel, morphemes] 값은 None일 수 없습니다."

        super().__init__(morphemes)
        self.surface = surface
        self.label = label
        self.fineLabel = fineLabel
        self.originalLabel = originalLabel
        self.reference = None

        for morph in self:
            morph.entities.append(self)

    def __setattr__(self, name, value):
        if name not in ['corefGroup', 'surface', 'label', 'fineLabel', 'originalLabel']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.Entity')(string(self.surface),
                                                           koala_enum_of('CoarseEntityType', self.label),
                                                           string(self.fineLabel),
                                                           java_list([m.getReference() for m in self]),
                                                           string(self.originalLabel))
        return self.reference

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 개체명의 표면형 문자열.
        """
        return self.surface

    def getLabel(self) -> CoarseEntityType:
        """
        :rtype: CoarseEntityType

        :return: 개체명 대분류 값, [CoarseEntityType]에 기록된 개체명 중 하나.
        """
        return CoarseEntityType.valueOf(self.label)

    def getFineLabel(self) -> str:
        """
        :rtype: str

        :return: 개체명 세분류 값으로, [label]으로 시작하는 문자열.
        """
        return self.fineLabel

    def getOriginalLabel(self) -> Optional[str]:
        """
        :rtype: str

        :return: 원본 분석기가 제시한 개체명 분류의 값. 기본값은 null.
        """
        return self.originalLabel

    def getCorefGroup(self):
        """
        이 개체명과 공통된 대상을 지칭하는 공통 지시어 또는 대용어들의 묶음을 제공합니다.

        참고:
            **공지시어 해소** 는 문장 내 또는 문장 간에 같은 대상을 지칭하는 어구를 찾아 묶는 분석과정입니다.

            예) '삼성그룹의 계열사인 삼성물산은 같은 그룹의 계열사인 삼성생명과 함께'라는 문장에서

            * '삼성그룹'과 '같은 그룹'을 찾아 묶는 것을 말합니다.

            **영형대용어 분석** 은 문장에서 생략된 기능어를 찾아 문장 내 또는 문장 간에 언급되어 있는 어구와 묶는 분석과정입니다.

            예) '나는 밥을 먹었고, 영희도 먹었다'라는 문장에서,

            * '먹었다'의 목적어인 '밥을'이 생략되어 있음을 찾는 것을 말합니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.CorefResolver` 공지시어 해소, 대용어 분석기 interface
            * :py:meth:`koalanlp.data.Sentence.getCorefGroups` 문장 내에 포함된 개체명 묶음 [CoreferenceGroup]들의 목록을 반환하는 API
            * :py:class:`koalanlp.data.CoreferenceGroup` 동일한 대상을 지칭하는 개체명을 묶는 API


        :rtype: CoreferenceGroup

        :return: 공통된 대상을 묶은 [CoreferenceGroup]. 없다면 None.
        """
        return self.corefGroup

    def __eq__(self, other):
        return self.label == other.label and self.fineLabel == other.fineLabel and super().__eq__(other)

    def __hash__(self):
        return hash(self.label) + hash(self.fineLabel) + sum(hash(x) for x in self)

    def __repr__(self):
        return "%s(%s; '%s')" % (str(self.label), self.fineLabel, self.surface)


class CoreferenceGroup(_PyListWrap):
    """
    공지시어 해소 또는 대용어 분석 결과를 저장할 class입니다.

    참고:
        **공지시어 해소** 는 문장 내 또는 문장 간에 같은 대상을 지칭하는 어구를 찾아 묶는 분석과정입니다.

        예) '삼성그룹의 계열사인 삼성물산은 같은 그룹의 계열사인 삼성생명과 함께'라는 문장에서

        * '삼성그룹'과 '같은 그룹'을 찾아 묶는 것을 말합니다.

        **영형대용어 분석** 은 문장에서 생략된 기능어를 찾아 문장 내 또는 문장 간에 언급되어 있는 어구와 묶는 분석과정입니다.

        예) '나는 밥을 먹었고, 영희도 먹었다'라는 문장에서,

        * '먹었다'의 목적어인 '밥을'이 생략되어 있음을 찾는 것을 말합니다.

        아래를 참고해보세요.
        * :py:class:`koalanlp.proc.CorefResolver` 공지시어 해소, 대용어 분석기 interface
        * :py:meth:`koalanlp.data.Sentence.getCorefGroups` 문장 내에 포함된 개체명 묶음 [CoreferenceGroup]들의 목록을 반환하는 API
        * :py:meth:`koalanlp.data.Entity.getCorefGroup` 각 개체명을 묶어 같은 지시 대상을 갖는 묶음인 [CoreferenceGroup]를 가져오는 API
    """

    def __init__(self, entities):
        """
        공지시어 해소 또는 대용어 분석 결과를 저장합니다.
        :param List[Entity] entities: 묶음에 포함되는 개체명들의 목록
        """
        super().__init__(entities)
        self.reference = None

        for entity in self:
            entity.corefGroup = self

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.CoreferenceGroup')(java_list([e.getReference() for e in self]))
        return self.reference


class Tree(_PyListWrap):
    """
    트리 구조를 저장할 [Property]입니다. :py:class:`Word`를 묶어서 표현하는 구조에 적용됩니다.
    """
    label = None
    terminal = None
    parent = None

    def __init__(self, label, terminal, children):
        """
        트리 형태의 구조를 저장합니다.
        :param label: 트리에 붙어있는 표지자입니다. None일 수 없습니다.
        :param Word terminal: 트리의 노드에서 연결되는 [Word]
        :param List[Tree] children: 트리/DAG의 자식 노드들
        """
        assert label is not None and children is not None, "[label, children]이 not None이어야 합니다."
        super().__init__(children)

        self.label = label
        self.terminal = terminal

    def __setattr__(self, name, value):
        if name not in ['label', 'terminal', 'children', 'parent']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getLabel(self):
        """
        트리에 붙어있는 표지자입니다. Null일 수 없습니다.

        :return: 표지자
        """
        return self.label

    def getTerminal(self):
        """

        :rtype: Word
        :return: 트리의 노드에서 연결되는 [Word] 또는 None
        """

        return self.terminal

    def isRoot(self) -> bool:
        """
        이 노드가 최상위 노드인지 확인합니다.

        :rtype: bool

        :return: 최상위 노드인 경우 true
        """
        return self.parent is None

    def hasNonTerminals(self) -> bool:
        """
        이 노드가 (terminal node를 제외하고) 자식 노드를 갖는지 확인합니다.

        * 구문분석 구조에서 terminal node는 [Word]가 됩니다.

        :rtype: bool

        :return: 자식노드가 있다면 True
        """
        return len(self) > 0

    def getTerminals(self):
        """
        이 노드를 포함해 모든 하위 Non-terminal 노드들에 속하는 terminal node들을 모읍니다.

        * 구문분석 구조에서는 이 구문구조에 속하는 어절의 모음입니다.


        :rtype: List[Word]

        :return: Terminal node의 목록
        """
        leaves = [term for child in self for term in child.getTerminals()]
        if self.getTerminal() is not None:
            leaves.append(self.getTerminal())

        return sorted(leaves, key=lambda x: x.getId())

    def getTreeString(self, depth=0, buffer='') -> str:
        """
        :rtype: str
        :param int depth: 들여쓰기할 수준입니다. 숫자만큼 들여쓰기됩니다. (기본값 0)
        :param str buffer: 결과를 저장할 버퍼입니다.
        :return: 트리구조의 표현을 문자열로 돌려줍니다.
        """

        buffer += ("| " * depth)
        buffer += str(self)

        for child in self:
            buffer += '\n'
            buffer = child.getTreeString(depth + 1, buffer)

        return buffer

    def getParent(self):
        """
        부모 노드를 반환합니다.

        * 부모 노드가 초기화되지 않은 경우 null을 반환합니다.

        :return: 같은 타입의 부모 노드 또는 null
        """
        return self.parent

    def getNonTerminals(self):
        """
        이 노드의 Non-terminal 자식 노드를 모읍니다.

        * 이 함수는 읽기의 편의를 위한 syntactic sugar입니다. 즉 다음 구문은 동일합니다.

        .. code-block:: python

            for item in x.getNonTerminals():
                ...
            for item in x:
                ...

        :return: 같은 타입의 부모 노드 또는 null
        """
        return self

    def __eq__(self, other):
        return self.label == other.label and self.terminal == other.terminal and super().__eq__(other)

    def __hash__(self):
        return hash(self.label) + (hash(self.terminal) if self.terminal is not None else 0) + sum(hash(x) for x in self)

    def __repr__(self):
        return "%s-Node(%s)" % (self.label, str(self.terminal) if self.terminal is not None else '')


class SyntaxTree(Tree):
    """
    구문구조 분석의 결과를 저장할 [Property].

    참고:
        **구문구조 분석** 은 문장의 구성요소들(어절, 구, 절)이 이루는 문법적 구조를 분석하는 방법입니다.

        예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는 2개의 절이 있습니다

        * 나는 밥을 먹었고
        * 영희는 짐을 쌌다

        각 절은 3개의 구를 포함합니다

        * 나는, 밥을, 영희는, 짐을: 체언구
        * 먹었고, 쌌다: 용언구

        아래를 참고해보세요.

        * :py:class:`koalanlp.proc.Parser` 구문구조 분석을 수행하는 interface.
        * :py:meth:`koalanlp.data.Word.getPhrase` 어절이 직접 속하는 가장 작은 구구조 [SyntaxTree]를 가져오는 API
        * :py:meth:`koalanlp.data.Sentence.getSyntaxTree` 전체 문장을 분석한 [SyntaxTree]를 가져오는 API
        * :py:class:`koalanlp.types.PhraseTag` 구구조의 형태 분류를 갖는 Enum 값
    """
    originalLabel = None  #: 원본 분석기의 표지자 값

    def __init__(self, label: str, terminal=None, children=None, originalLabel=None):
        """
        구문구조 분석의 결과를 생성합니다.

        :param str label: 구구조 표지자입니다. [PhraseTag] Enum 값입니다.
        :param Word terminal: 현재 구구조에 직접 속하는 [Word]들. 중간 구문구조인 경우 leaf를 직접 포함하지 않으므로 None.
        :param List[SyntaxTree] children: 현재 구구조에 속하는 하위 구구조 [SyntaxTree]. 하위 구구조가 없다면 빈 리스트.
        :param str originalLabel: 원본 분석기의 표지자 String 값. 기본값은 None.
        """
        children = children if children is not None else []
        super().__init__(label, terminal, children)

        self.originalLabel = originalLabel
        self.reference = None

        term = self.getTerminal()
        if term is not None:
            term.phrase = self

        for child in self:
            child.parent = self

    def __setattr__(self, name, value):
        if name not in ['label', 'terminal', 'children', 'parent', 'originalLabel']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.SyntaxTree')(koala_enum_of('PhraseTag', self.label),
                                                               self.terminal.getReference() if self.terminal is not None else None,
                                                               java_list([t.getReference() for t in self]),
                                                               string(self.originalLabel))
        return self.reference

    def getOriginalLabel(self) -> Optional[str]:
        """

        :rtype: str

        :return: 원본 분석기의 표지자 String 값. 기본값은 None.
        """
        return self.originalLabel

    def getLabel(self) -> PhraseTag:
        """

        :rtype: PhraseTag

        :return: 구문구조 표지자
        """
        return PhraseTag.valueOf(super().getLabel())


class DAGEdge(object):
    """
    DAG Edge를 저장합니다.
    """
    src = None  #: Edge의 시작점.
    dest = None  #: Edge의 종점.
    label = None  #: Edge가 나타내는 관계

    def __init__(self, src, dest, label):
        assert dest is not None, "[dest]이 not None이어야 합니다."
        self.src = src
        self.dest = dest
        self.label = label

    def __setattr__(self, name, value):
        if name not in ['src', 'dest', 'label']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getSrc(self):
        """
        :return: Edge의 시작점. 의존구문분석인 경우 지배소, 의미역인 경우 동사.
        """
        return self.src

    def getDest(self):
        """
        :return: Edge의 종점. 의존구문분석인 경우 피지배소, 의미역인 경우 논항.
        """
        return self.dest

    def getLabel(self):
        """
        :return: Edge가 나타내는 관계.
        """
        return self.label

    def __eq__(self, other):
        return type(self) is type(other) and self.label == other.label and \
               self.src == other.src and self.dest == other.dest

    def __hash__(self):
        return (hash(self.label) if self.label is not None else 0) + \
               hash(self.dest) + (hash(self.src) if self.src is not None else 0)

    def __repr__(self):
        return "%s('%s' → '%s')" % (str(self.label) if self.label is not None else '',
                                    str(self.src) if self.src is not None else 'ROOT',
                                    str(self.dest))


class DepEdge(DAGEdge):
    """
    의존구문구조 분석의 결과.

    참고:
        **의존구조 분석** 은 문장의 구성 어절들이 의존 또는 기능하는 관계를 분석하는 방법입니다.

        예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는

        가장 마지막 단어인 '쌌다'가 핵심 어구가 되며,

        * '먹었고'가 '쌌다'와 대등하게 연결되고
        * '나는'은 '먹었고'의 주어로 기능하며
        * '밥을'은 '먹었고'의 목적어로 기능합니다.
        * '영희는'은 '쌌다'의 주어로 기능하고,
        * '짐을'은 '쌌다'의 목적어로 기능합니다.

        아래를 참고해보세요.

        * :py:class:`koalanlp.proc.Parser` 의존구조 분석을 수행하는 interface.
        * :py:meth:`koalanlp.data.Word.getDependentEdges` 어절이 직접 지배하는 하위 의존구조 [DepEdge]의 목록을 가져오는 API
        * :py:meth:`koalanlp.data.Word.getGovernorEdge` 어절이 지배당하는 상위 의존구조 [DepEdge]를 가져오는 API
        * :py:meth:`koalanlp.data.Sentence.getDependencies` 전체 문장을 분석한 의존구조 [DepEdge]의 목록을 가져오는 API
        * :py:meth:`koalanlp.types.PhraseTag` 의존구조의 형태 분류를 갖는 Enum 값 (구구조 분류와 같음)
        * :py:meth:`koalanlp.types.DependencyTag` 의존구조의 기능 분류를 갖는 Enum 값
    """
    originalLabel = None  #: 원본 분석기의 표지자 값
    type = None  #: 구문구조 표지자 값
    governor = None  #: 의존구문구조의 지배소
    dependent = None  #: 의존구문구조의 피지배소
    depType = None  #: 의존구문구조 표지자 값

    def __init__(self, governor, dependent, type: str, depType: str = None, originalLabel: str = None):
        """
        의존구문 구조를 생성합니다.
        :param Word governor: 의존구문구조의 지배소
        :param Word dependent: 의존구문구조의 피지배소
        :param str type: 구문분석 표지자
        :param str depType: 의존구문구조 표지자
        :param str originalLabel: 의존구문구조 표지자의 원본분석기 표기
        """
        assert type is not None, "type은 None일 수 없습니다."
        super().__init__(governor, dependent, depType)
        self.type = type
        self.depType = self.label
        self.originalLabel = originalLabel

        if self.dest is not None:
            self.dest.governorEdge = self

        if self.src is not None:
            self.src.dependentEdges.append(self)

        self.governor = self.src
        self.dependent = self.dest
        self.reference = None

    def __setattr__(self, name, value):
        if name not in ['src', 'dest', 'governor', 'dependent', 'label', 'type', 'depType', 'originalLabel']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.DepEdge')(
                self.governor.getReference() if self.governor is not None else None,
                self.dependent.getReference(),
                koala_enum_of('PhraseTag', self.type),
                koala_enum_of('DependencyTag', self.depType),
                string(self.originalLabel))
        return self.reference

    def getGovernor(self):
        """

        :rtype: Word

        :return: 의존구조의 지배소 [Word]. 문장의 Root에 해당하는 경우 None.
        """
        return self.src

    def getDependent(self):
        """

        :rtype: Word

        :return: 의존구조의 피지배소 [Word]
        """
        return self.dest

    def getDepType(self) -> Optional[DependencyTag]:
        """

        :rtype: DependencyTag

        :return: 의존기능 표지자, [DependencyTag] Enum 값. 별도의 기능이 지정되지 않으면 None. (ETRI 표준안은 구구조+의존기능으로 의존구문구조를 표기함)
        """
        return DependencyTag.valueOf(self.label) if self.label is not None else None

    def getType(self) -> PhraseTag:
        """

        :rtype: PhraseTag

        :return: 구구조 표지자, [PhraseTag] Enum 값 (ETRI 표준안은 구구조+의존기능으로 의존구문구조를 표기함)
        """
        return PhraseTag.valueOf(self.type)

    def getOriginalLabel(self) -> Optional[str]:
        """

        :rtype: str

        :return: 원본 분석기의 표지자 String 값. 기본값은 None.
        """
        return self.originalLabel

    def getLabel(self) -> DependencyTag:
        """
        :rtype: DependencyTag
        :return: Edge가 나타내는 관계.
        """
        return DependencyTag.valueOf(self.label) if self.label is not None else None

    def __repr__(self):
        return "%s%s" % (str(self.type), super().__repr__())

    def __eq__(self, other):
        return self.type == other.type and super().__eq__(other)

    def __hash__(self):
        return hash(self.type) + super().__hash__()


class RoleEdge(DAGEdge):
    """
    의미역 구조 분석의 결과.

    참고:
        **의미역 결정** 은 문장의 구성 어절들의 역할/기능을 분석하는 방법입니다.

        예) '나는 밥을 어제 집에서 먹었다'라는 문장에는

        동사 '먹었다'를 중심으로

        * '나는'은 동작의 주체를,
        * '밥을'은 동작의 대상을,
        * '어제'는 동작의 시점을
        * '집에서'는 동작의 장소를 나타냅니다.

        아래를 참고해보세요.

        * :py:class:`koalanlp.proc.RoleLabeler` 의미역 분석을 수행하는 interface.
        * :py:meth:`koalanlp.data.Word.getArgumentRoles` 어절이 술어인 논항들의 [RoleEdge] 목록을 가져오는 API
        * :py:meth:`koalanlp.data.Word.getPredicateRoles` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
        * :py:meth:`koalanlp.data.Sentence.getRoles` 전체 문장을 분석한 의미역 구조 [RoleEdge]를 가져오는 API
        * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값
    """
    originalLabel = None  #: 원본 분석기의 표지자 값
    modifiers = []  #: 논항의 수식어구 목록.
    predicate = None  #: 의미역 구조의 술어
    argument = None  #: 의미역 구조의 논항

    def __init__(self, predicate, argument, label: str, modifiers: List = None, originalLabel: str = None):
        """
        의미역 구조를 생성합니다.
        :param Word predicate: 의미역 구조의 술어
        :param Word argument: 의미역 구조의 논항
        :param str label: 의미역 구조의 표지자
        :param List[Word] modifiers: 논항의 수식어구들
        :param str originalLabel: 의미역 구조 표지자의 원본분석기 표기
        """
        assert predicate is not None and label is not None, "[predicate, label]은 not None이어야 합니다."
        super().__init__(predicate, argument, label)

        self.modifiers = modifiers if modifiers is not None else []
        self.originalLabel = originalLabel

        if self.dest is not None:
            self.dest.predicateRole = self

        if self.src is not None:
            self.src.argumentRoles.append(self)

        self.predicate = self.src
        self.argument = self.dest
        self.reference = None

    def __setattr__(self, name, value):
        if name not in ['src', 'dest', 'predicate', 'argument', 'label', 'modifiers', 'originalLabel']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.RoleEdge')(
                self.predicate.getReference() if self.predicate is not None else None,
                self.argument.getReference(),
                koala_enum_of('RoleType', self.label),
                java_list([w.getReference() for w in self.modifiers]),
                string(self.originalLabel))
        return self.reference

    def getPredicate(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 표현하는 동사 [Word]
        """
        return self.src

    def getArgument(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 서술된 논항 [Word]
        """
        return self.dest

    def getModifiers(self) -> List:
        """

        :rtype: List[Word]

        :return: 논항의 수식어구들
        """
        return self.modifiers

    def getOriginalLabel(self) -> Optional[str]:
        """

        :rtype: str

        :return: 원본 분석기의 표지자 String 값. 기본값은 None.
        """
        return self.originalLabel

    def getLabel(self) -> RoleType:
        """
        :rtype: RoleType
        :return: Edge가 나타내는 관계.
        """
        return RoleType.valueOf(self.label)

    def __repr__(self):
        return "%s('%s' → '%s/%s')" % (str(self.label) if self.label is not None else '',
                                       self.src.surface if self.src is not None else 'ROOT',
                                       self.dest.surface,
                                       ' '.join(w.surface for w in self.modifiers))


class Morpheme(object):
    """
    형태소를 저장하는 [Property] class입니다.

    참고:
        **형태소** 는 의미를 가지는 요소로서는 더 이상 분석할 수 없는 가장 작은 말의 단위로 정의됩니다.

        **형태소 분석** 은 문장을 형태소의 단위로 나누는 작업을 의미합니다.

        예) '문장을 형태소로 나눠봅시다'의 경우,

        * 문장/일반명사, -을/조사,
        * 형태소/일반명사, -로/조사,
        * 나누-(다)/동사, -어-/어미, 보-(다)/동사, -ㅂ시다/어미

        로 대략 나눌 수 있습니다.

        아래를 참고해보세요.

        * :py:class:`koalanlp.proc.CanTag` 형태소 분석기의 최상위 Interface
        * :py:class:`koalanlp.types.POS` 형태소의 분류를 담은 Enum class
    """

    surface = ''  #: 형태소 표면형
    id = None  #: 형태소의 어절 내 위치
    tag = None  #: 형태소의 세종 품사
    originalTag = None  #: 형태소의 원본분석기 품사
    word = None  #: 형태소의 상위 어절.
    wordSense = None  #: 형태소의 의미 어깨번호. :py:meth:`getWordSense` 참고.
    entities = []  #: 형태소를 포함하는 개체명 목록. :py:meth:`getEntities` 참고.

    def __init__(self, surface: str, tag: str, originalTag: str = None, reference=None):
        """
        형태소를 생성합니다.
        :param str surface: 형태소 표면형
        :param str tag: 형태소 품사 태그
        :param str originalTag: 형태소 품사 원본 표기
        """
        assert surface is not None and tag is not None, "surface, tag가 None이 아니어야 합니다."

        self.surface = surface
        self.tag = tag
        self.originalTag = originalTag
        self.reference = reference
        self.id = None
        self.word = None
        self.wordSense = None
        self.entities = []

        if self.reference.getWordSense() is not None:
            self.wordSense = self.reference.getWordSense()

    def __setattr__(self, name, value):
        if name not in ['surface', 'tag', 'originalTag', 'id', 'word']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.Morpheme')(
                string(self.surface),
                koala_enum_of('POS', self.tag),
                string(self.originalTag))
        return self.reference

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 형태소 표면형 String
        """
        return self.surface

    def getOriginalTag(self) -> Optional[str]:
        """

        :rtype: str

        :return: 원본 형태소 분석기의 품사 String (없으면 None)
        """
        return self.originalTag

    def getTag(self) -> POS:
        """

        :rtype: POS

        :return: 세종 품사표기
        """
        return POS.valueOf(self.tag)

    def getId(self) -> int:
        """

        :rtype: int

        :return: 형태소의 어절 내 위치입니다.
        """
        return self.id

    def getWordSense(self) -> Optional[int]:
        """
        다의어 분석 결과인, 이 형태소의 사전 속 의미/어깨번호 값을 돌려줍니다.

        다의어 분석을 한 적이 없다면 None을 돌려줍니다.


        :rtype: int

        :return: 의미/어깨번호 값
        """
        return self.wordSense

    def getEntities(self) -> List[Entity]:
        """
        개체명 분석을 했다면, 현재 형태소가 속한 개체명 값을 돌려줍니다.

        참고:
            **개체명 인식** 은 문장에서 인물, 장소, 기관, 대상 등을 인식하는 기술입니다.

            예) '철저한 진상 조사를 촉구하는 국제사회의 목소리가 커지고 있는 가운데, 트럼프 미국 대통령은 되레 사우디를 감싸고 나섰습니다.'에서, 다음을 인식하는 기술입니다.

            * '트럼프': 인물
            * '미국' : 국가
            * '대통령' : 직위
            * '사우디' : 국가

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.EntityRecognizer` 개체명 인식기 interface
            * :py:meth:`koalanlp.data.Word.getEntities` 어절에 연관된 모든 [Entity]를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getEntities` 문장에 포함된 모든 [Entity]를 가져오는 API
            * :py:class:`koalanlp.data.Entity` 개체명을 저장하는 형태
            * :py:class:`koalanlp.types.CoarseEntityType` [Entity]의 대분류 개체명 분류구조 Enum 값


        :rtype: List[Entity]

        :return: [Entity]의 목록입니다. 분석 결과가 없으면 빈 리스트
        """
        return self.entities

    def getWord(self):
        """

        :rtype: Word

        :return: 이 형태소를 포함하는 단어를 돌려줍니다.
        """
        return self.word

    def isNoun(self) -> bool:
        """
        체언(명사, 수사, 대명사) 형태소인지 확인합니다.

        :rtype: bool

        :return: 체언이라면 true
        """

        return self.getTag().isNoun()

    def isPredicate(self) -> bool:
        """
        용언(동사, 형용사) 형태소인지 확인합니다.

        :rtype: bool

        :return: 용언이라면 true
        """

        return self.getTag().isPredicate()

    def isModifier(self) -> bool:
        """
        수식언(관형사, 부사) 형태소인지 확인합니다.

        :rtype: bool

        :return: 수식언이라면 true
        """

        return self.getTag().isModifier()

    def isJosa(self) -> bool:
        """
        관계언(조사) 형태소인지 확인합니다.

        :rtype: bool

        :return: 관계언이라면 true
        """

        return self.getTag().isPostPosition()

    def hasTag(self, partialTag: str) -> bool:
        """
        세종 품사 [tag]가 주어진 품사 표기 [partialTag] 묶음에 포함되는지 확인합니다.

        예) "N"은 체언인지 확인하고, "NP"는 대명사인지 확인

        단축명령:
            * 체언(명사, 수사, 대명사) :py:meth:`isNoun`
            * 용언(동사, 형용사)는 :py:meth:`isPredicate`
            * 수식언(관형사, 부사)는 :py:meth:`isModifier`
            * 관계언(조사)는 :py:meth:`isJosa`

        참고:
            * 분석불능범주(NA, NV, NF)는 체언(N) 범주에 포함되지 않습니다.
            * 세종 품사표기는 `POS <https://koalanlp.github.io/koalanlp/api/koalanlp/kr.bydelta.koala/-p-o-s/index.html>` 를 참고하세요.
            * 품사 표기는 `비교표 <https://docs.google.com/spreadsheets/d/1OGM4JDdLk6URuegFKXg1huuKWynhg_EQnZYgTmG4h0s/edit?usp=sharing>` 에서 확인가능합니다.


        :param str partialTag: 포함 여부를 확인할 상위 형태소 분류 품사표기

        :rtype: bool

        :return: 포함되는 경우 True.
        """
        return self.getTag().startsWith(partialTag)

    def hasTagOneOf(self, *tags: str) -> bool:
        """
        세종 품사 [tag]가 주어진 품사 표기들 [tags] 묶음들 중 하나에 포함되는지 확인합니다.

        예) hasTagOneOf("N", "MM")의 경우, 체언 또는 관형사인지 확인합니다.

        단축명령:
            * 체언(명사, 수사, 대명사) :py:meth:`isNoun`
            * 용언(동사, 형용사)는 :py:meth:`isPredicate`
            * 수식언(관형사, 부사)는 :py:meth:`isModifier`
            * 관계언(조사)는 :py:meth:`isJosa`

        참고:
            * 분석불능범주(NA, NV, NF)는 체언(N) 범주에 포함되지 않습니다.
            * 세종 품사표기는 `POS <https://koalanlp.github.io/koalanlp/api/koalanlp/kr.bydelta.koala/-p-o-s/index.html>` 를 참고하세요.
            * 품사 표기는 `비교표 <https://docs.google.com/spreadsheets/d/1OGM4JDdLk6URuegFKXg1huuKWynhg_EQnZYgTmG4h0s/edit?usp=sharing>` 에서 확인가능합니다.


        :param str partialTag: 포함 여부를 확인할 상위 형태소 분류 품사표기들 (가변인자)

        :rtype: bool

        :return: 하나라도 포함되는 경우 True.
        """
        return any(self.getTag().startsWith(t) for t in tags)

    def hasOriginalTag(self, partialTag: str) -> bool:
        """
        원본 품사 [originalTag]가 주어진 품사 표기 [partialTag] 묶음에 포함되는지 확인합니다.

        지정된 원본 품사가 없으면 (즉, None이면) false를 반환합니다.

        단축명령:
            * 체언(명사, 수사, 대명사) :py:meth:`isNoun`
            * 용언(동사, 형용사)는 :py:meth:`isPredicate`
            * 수식언(관형사, 부사)는 :py:meth:`isModifier`
            * 관계언(조사)는 :py:meth:`isJosa`

        참고:
            * 분석불능범주(NA, NV, NF)는 체언(N) 범주에 포함되지 않습니다.
            * 세종 품사표기는 `POS <https://koalanlp.github.io/koalanlp/api/koalanlp/kr.bydelta.koala/-p-o-s/index.html>` 를 참고하세요.
            * 품사 표기는 `비교표 <https://docs.google.com/spreadsheets/d/1OGM4JDdLk6URuegFKXg1huuKWynhg_EQnZYgTmG4h0s/edit?usp=sharing>` 에서 확인가능합니다.


        :param str partialTag: 포함 여부를 확인할 상위 형태소 분류 품사표기

        :rtype: bool

        :return: 포함되는 경우 True.
        """
        return self.originalTag.upper().startswith(partialTag.upper()) if self.originalTag is not None else False

    def equalsWithoutTag(self, other):
        """
        타 형태소 객체 [another]와 형태소의 표면형이 같은지 비교합니다.

        :param Morpheme other: 표면형을 비교할 형태소

        :rtype: bool

        :return: 표면형이 같으면 True
        """
        return self.surface == other.surface

    def __eq__(self, other):
        return type(other) is Morpheme and self.surface == other.surface and self.tag == other.tag

    def __hash__(self):
        return hash(self.surface) * len(POS.values()) + hash(self.tag)

    def __repr__(self):
        return "%s/%s(%s)" % (self.surface, str(self.tag), self.originalTag) if self.originalTag is not None \
            else "%s/%s" % (self.surface, str(self.tag))


class Word(_PyListWrap):
    """
    어절을 표현하는 [Property] class입니다.
    """
    surface = ''  #: 어절의 표면형
    id = None  #: 어절의 문장 내 위치
    morphemes = []  #: 어절 내 형태소 목록
    entities = []  #: 개체명 분석을 했다면, 현재 어절이 속한 개체명 값. :py:meth:`getEntities` 참고
    phrase = None  #: 구문분석을 했다면, 현재 어절이 속한 직속 상위 구구조(Phrase). :py:meth:`getPhrase` 참고
    dependentEdges = []  #: 의존구문분석을 했다면, 현재 어절이 지배소인 하위 의존구문 구조의 값. :py:meth:`getDependentEdges` 참고.
    governorEdge = None  #: 의존구문분석을 했다면, 현재 어절이 의존소인 상위 의존구문 구조의 값. :py:meth:`getGovernorEdge` 참고
    argumentRoles = []  #: 의미역 분석을 했다면, 현재 어절이 술어로 기능하는 하위 의미역 구조의 목록. :py:meth:`getArgumentRoles` 참고.
    predicateRoles = []  #: 의미역 분석을 했다면, 현재 어절이 논항인 상위 의미역 구조의 목록. :py:meth:`getPredicateRoles` 참고.

    def __init__(self, surface, morphemes, reference=None):
        """
        어절을 생성합니다.
        :param str surface: 어절의 표면형
        :param List[Morpheme] morphemes: Morpheme 목록으로부터 문장을 만들 때, List[Morpheme]
        """
        assert surface is not None and morphemes is not None and len(morphemes) > 0, \
            "morphemes가 list이고, surface가 None이 아니어야 합니다."

        self.surface = surface
        self.morphemes = morphemes
        self.reference = reference
        self.id = None
        self.entities = []
        self.phrase = None
        self.dependentEdges = []
        self.governorEdge = None
        self.argumentRoles = []
        self.predicateRoles = []
        super().__init__(self.morphemes)

        for i, morph in enumerate(self):
            morph.word = self
            morph.id = i

    def __setattr__(self, name, value):
        if name not in ['surface', 'morphemes', 'id']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.Word')(
                string(self.surface),
                java_list([m.getReference() for m in self]))
        return self.reference

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 어절의 표면형 String.
        """
        return self.surface

    def getId(self) -> int:
        """

        :rtype: int

        :return: 어절의 문장 내 위치입니다.
        """
        return self.id

    def getEntities(self) -> List[Entity]:
        """
        개체명 분석을 했다면, 현재 어절이 속한 개체명 값을 돌려줍니다.

        참고:
            **개체명 인식** 은 문장에서 인물, 장소, 기관, 대상 등을 인식하는 기술입니다.

            예) '철저한 진상 조사를 촉구하는 국제사회의 목소리가 커지고 있는 가운데, 트럼프 미국 대통령은 되레 사우디를 감싸고 나섰습니다.'에서, 다음을 인식하는 기술입니다.

            * '트럼프': 인물
            * '미국' : 국가
            * '대통령' : 직위
            * '사우디' : 국가

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.EntityRecognizer` 개체명 인식기 interface
            * :py:meth:`koalanlp.data.Morpheme.getEntities` 형태소를 포함하는 모든 [Entity]를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getEntities` 문장에 포함된 모든 [Entity]를 가져오는 API
            * :py:class:`koalanlp.data.Entity` 개체명을 저장하는 형태
            * :py:class:`koalanlp.types.CoarseEntityType` [Entity]의 대분류 개체명 분류구조 Enum 값

        :rtype: List[Entity]

        :return: [Entity]의 목록입니다. 분석 결과가 없으면 빈 리스트.
        """
        value = set()
        for morph in self:
            if morph.getEntities() is not None:
                for ent in morph.getEntities():
                    value.add(ent)

        return list(value)

    def getPhrase(self) -> SyntaxTree:
        """
        구문분석을 했다면, 현재 어절이 속한 직속 상위 구구조(Phrase)를 돌려줍니다.

        참고:
            **구문구조 분석** 은 문장의 구성요소들(어절, 구, 절)이 이루는 문법적 구조를 분석하는 방법입니다.

            예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는 2개의 절이 있습니다

            * 나는 밥을 먹었고
            * 영희는 짐을 쌌다

            각 절은 3개의 구를 포함합니다

            * 나는, 밥을, 영희는, 짐을: 체언구
            * 먹었고, 쌌다: 용언구

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.Parser` 구문구조 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Sentence.getSyntaxTree` 전체 문장을 분석한 [SyntaxTree]를 가져오는 API
            * :py:class:`koalanlp.data.SyntaxTree` 구문구조를 저장하는 형태
            * :py:class:`koalanlp.types.PhraseTag` 구구조의 형태 분류를 갖는 Enum 값

        :rtype: SyntaxTree

        :return: 어절의 상위 구구조 [SyntaxTree]. 분석 결과가 없으면 None
        """
        return self.phrase

    def getDependentEdges(self) -> List[DepEdge]:
        """
        의존구문분석을 했다면, 현재 어절이 지배소인 하위 의존구문 구조의 값을 돌려줍니다.

        참고:
            **의존구조 분석** 은 문장의 구성 어절들이 의존 또는 기능하는 관계를 분석하는 방법입니다.

            예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는

            가장 마지막 단어인 '쌌다'가 핵심 어구가 되며,

            * '먹었고'가 '쌌다'와 대등하게 연결되고
            * '나는'은 '먹었고'의 주어로 기능하며
            * '밥을'은 '먹었고'의 목적어로 기능합니다.
            * '영희는'은 '쌌다'의 주어로 기능하고,
            * '짐을'은 '쌌다'의 목적어로 기능합니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.Parser` 의존구조 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getGovernorEdge` 어절이 지배당하는 상위 의존구조 [DepEdge]를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getDependencies` 전체 문장을 분석한 의존구조 [DepEdge]의 목록을 가져오는 API
            * :py:meth:`koalanlp.types.PhraseTag` 의존구조의 형태 분류를 갖는 Enum 값 (구구조 분류와 같음)
            * :py:meth:`koalanlp.types.DependencyTag` 의존구조의 기능 분류를 갖는 Enum 값
            * :py:class:`koalanlp.data.DepEdge` 의존구문구조의 저장형태

        :rtype: List[DepEdge]

        :return: 어절이 지배하는 의존구문구조 [DepEdge]의 목록. 분석 결과가 없으면 빈 리스트.
        """
        return self.dependentEdges

    def getGovernorEdge(self) -> DepEdge:
        """
        의존구문분석을 했다면, 현재 어절이 의존소인 상위 의존구문 구조의 값을 돌려줍니다.

        참고:
            **의존구조 분석** 은 문장의 구성 어절들이 의존 또는 기능하는 관계를 분석하는 방법입니다.

            예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는

            가장 마지막 단어인 '쌌다'가 핵심 어구가 되며,

            * '먹었고'가 '쌌다'와 대등하게 연결되고
            * '나는'은 '먹었고'의 주어로 기능하며
            * '밥을'은 '먹었고'의 목적어로 기능합니다.
            * '영희는'은 '쌌다'의 주어로 기능하고,
            * '짐을'은 '쌌다'의 목적어로 기능합니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.Parser` 의존구조 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getDependentEdges` 어절이 직접 지배하는 하위 의존구조 [DepEdge]의 목록를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getDependencies` 전체 문장을 분석한 의존구조 [DepEdge]의 목록을 가져오는 API
            * :py:meth:`koalanlp.types.PhraseTag` 의존구조의 형태 분류를 갖는 Enum 값 (구구조 분류와 같음)
            * :py:meth:`koalanlp.types.DependencyTag` 의존구조의 기능 분류를 갖는 Enum 값
            * :py:class:`koalanlp.data.DepEdge` 의존구문구조의 저장형태

        :rtype: List[DepEdge]

        :return: 어절이 지배당하는 의존구문구조 [DepEdge]. 분석 결과가 없으면 None
        """
        return self.governorEdge

    def getArgumentRoles(self) -> List[RoleEdge]:
        """
        의미역 분석을 했다면, 현재 어절이 술어로 기능하는 하위 의미역 구조의 목록을 돌려줌.

        참고:
            **의미역 결정** 은 문장의 구성 어절들의 역할/기능을 분석하는 방법입니다.

            예) '나는 밥을 어제 집에서 먹었다'라는 문장에는

            동사 '먹었다'를 중심으로

            * '나는'은 동작의 주체를,
            * '밥을'은 동작의 대상을,
            * '어제'는 동작의 시점을
            * '집에서'는 동작의 장소를 나타냅니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.RoleLabeler` 의미역 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getPredicateRoles` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getRoles` 전체 문장을 분석한 의미역 구조 [RoleEdge]를 가져오는 API
            * :py:class:`koalanlp.data.RoleEdge` 의미역 구조를 저장하는 형태
            * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값

        :rtype: List[RoleEdge]

        :return: 어절이 술어로 기능하는 하위 의미역 구조 [RoleEdge]의 목록. 분석 결과가 없으면 빈 리스트.
        """
        return self.argumentRoles

    def getPredicateRoles(self) -> RoleEdge:
        """
        의미역 분석을 했다면, 현재 어절이 논항인 상위 의미역 구조를 돌려줌.

        참고:
            **의미역 결정** 은 문장의 구성 어절들의 역할/기능을 분석하는 방법입니다.

            예) '나는 밥을 어제 집에서 먹었다'라는 문장에는

            동사 '먹었다'를 중심으로

            * '나는'은 동작의 주체를,
            * '밥을'은 동작의 대상을,
            * '어제'는 동작의 시점을
            * '집에서'는 동작의 장소를 나타냅니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.RoleLabeler` 의미역 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getArgumentRoles` 어절이 술어인 논항들의 [RoleEdge] 목록을 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getRoles` 전체 문장을 분석한 의미역 구조 [RoleEdge]를 가져오는 API
            * :py:class:`koalanlp.data.RoleEdge` 의미역 구조를 저장하는 형태
            * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값

        :rtype: RoleEdge

        :return: 어절이 논항인 상위 의미역 구조 [RoleEdge]. 분석 결과가 없으면 None.
        """
        return self.predicateRoles

    def singleLineString(self) -> str:
        """
        품사분석 결과를, 1행짜리 String으로 변환합니다.

        예) '나/NP+는/JX'

        참고:
            * 세종 품사표기는 :py:class:`koalanlp.types.POS` 를 참고하세요.

        :return: 각 형태소별로 "표면형/품사" 형태로 기록하고 이를 +로 이어붙인 문자열.
        """
        return "+".join("%s/%s" % (it.surface, it.tag) for it in self)

    def equalsWithoutTag(self, other) -> bool:
        """
        [other] 어절과 표면형이 같은지 비교합니다.
        :param Word other: 표면형을 비교할 다른 어절
        :rtype: bool
        :return: 표면형이 같으면 true
        """
        return self.surface == other.surface

    def __repr__(self) -> str:
        """
        문자열 표현을 생성합니다.

        :rtype: str
        :return: 이 객체의 문자열 표현
        """
        return "%s = %s" % (self.surface, self.singleLineString())

    def __hash__(self):
        return hash(self.surface) + super().__hash__()

    def __eq__(self, other):
        return self.surface == other.surface and super().__eq__(other)


class Sentence(_PyListWrap):
    """
    문장을 표현하는 [Property] class입니다.
    """
    words = []  #: 문장내 어절의 목록
    syntaxTree = None  #: 문장의 최상위 구구조 (분석결과가 없으면 None) :py:meth:`getSyntaxTree` 참고.
    dependencies = []  #: 문장에 포함된 모든 의존구문구조 (분석결과가 없으면 []). :py:meth:`getDependencies` 참고
    roles = []  #: 문장에 포함된 모든 의미역 구조 (분석 결과가 없으면 []). :py:meth:`getRoles` 참고
    entities = []  #: 문장에 포함된 모든 개체명 (분석 결과가 없으면 []). :py:meth:`getEntities` 참고
    corefGroups = []  #: 문장 내에 포함된 공통 지시어 또는 대용어들의 묶음 (분석 결과가 없으면 []). :py:meth:`getCorefGroups` 참고
    reference = None  #: Java 문장 타입

    def __init__(self, words=None, reference=None):
        """
        문장을 생성합니다.
        :param List[Word] words: Word의 목록으로부터 문장을 만들 때, List[word]
        :param reference: Java 분석 결과로부터 문장을 만들 때, Java KoalaNLP의 Sentence
        """
        assert (words is not None and len(words) > 0) or reference is not None, \
            "words가 list이거나 reference가 None이 아니어야 합니다."

        if reference is not None:
            self.words = py_list(reference,
                                 lambda w: Word(surface=w.getSurface(),
                                                morphemes=py_list(w,
                                                                  lambda m: Morpheme(surface=m.getSurface(),
                                                                                     tag=m.getTag().name(),
                                                                                     originalTag=m.getOriginalTag(),
                                                                                     reference=m)),
                                                reference=w))
            super().__init__(self.words)

            obj = reference.getSyntaxTree()
            self.syntaxTree = self.__recon_syntax_tree(obj)
            self.dependencies = py_list(reference.getDependencies(), self.__get_dep_edge)
            self.roles = py_list(reference.getRoles(), self.__get_role)
            self.entities = py_list(reference.getEntities(), self.__get_entity)
            self.corefGroups = py_list(reference.getCorefGroups(), self.__get_coref)
            self.reference = reference
        else:
            self.words = words
            self.syntaxTree = None
            self.dependencies = []
            self.roles = []
            self.entities = []
            self.corefGroups = []
            self.reference = None
            super().__init__(words)

        for i, word in enumerate(self):
            word.id = i

    def __setattr__(self, name, value):
        if name not in ['words', 'syntaxTree', 'dependencies', 'roles', 'entities', 'corefGroups']:
            pass
        elif name not in self.__dict__:
            pass
        elif getattr(self, name) is None or len(getattr(self, name)) == 0:
            pass
        else:
            raise AttributeError("Can't touch {}".format(name))

        super().__setattr__(name, value)

    def __get_jword(self, jword) -> Optional[Word]:
        if jword is not None:
            return self[jword.getId()]
        else:
            return None

    def __get_jmorph(self, jmorph) -> Optional[Morpheme]:
        if jmorph is not None:
            return self[jmorph.getWord().getId()][jmorph.getId()]
        else:
            return None

    def __recon_syntax_tree(self, jtree) -> Optional[SyntaxTree]:
        if jtree is None:
            return None

        jtree = koala_cast_of(jtree, 'data.SyntaxTree')
        term = None
        non_terms = None

        if jtree.getTerminal() is not None:
            term = self.__get_jword(jtree.getTerminal())

        if jtree.hasNonTerminals():
            non_terms = py_list(jtree, self.__recon_syntax_tree)

        tree = SyntaxTree(label=jtree.getLabel().name(), terminal=term,
                          children=non_terms, originalLabel=jtree.getOriginalLabel())
        tree.reference = jtree
        return tree

    def __get_dep_edge(self, e) -> DepEdge:
        edge = DepEdge(governor=self.__get_jword(e.getGovernor()),
                       dependent=self.__get_jword(e.getDependent()),
                       type=e.getType().name(),
                       depType=e.getDepType().name() if e.getDepType() is not None else None,
                       originalLabel=e.getOriginalLabel())
        edge.reference = e
        return edge

    def __get_role(self, e) -> RoleEdge:
        edge = RoleEdge(predicate=self.__get_jword(e.getPredicate()),
                        argument=self.__get_jword(e.getArgument()),
                        label=e.getLabel().name(),
                        modifiers=py_list(e.getModifiers(), self.__get_jword),
                        originalLabel=e.getOriginalLabel())
        edge.reference = e
        return edge

    def __get_entity(self, e) -> Entity:
        enty = Entity(surface=e.getSurface(), label=e.getLabel().name(),
                      fineLabel=e.getFineLabel(), morphemes=py_list(e, self.__get_jmorph),
                      originalLabel=e.getOriginalLabel())
        enty.reference = e
        return enty

    def __get_coref(self, c) -> CoreferenceGroup:
        coref = CoreferenceGroup(py_list(c, lambda e: self.entities[self.entities.index(self.__get_entity(e))]))
        coref.reference = c
        return coref

    def getReference(self):
        if self.reference is None:
            self.reference = koala_class_of('data.Sentence')(java_list([w.getReference() for w in self]))

        if self.getSyntaxTree() is not None and self.reference.getSyntaxTree() is None:
            self.reference.setSyntaxTree(self.getSyntaxTree().getReference())

        if len(self.getRoles()) > 0 and self.reference.getRoles() is None:
            self.reference.setRoleEdges(java_list([e.getReference() for e in self.getRoles()]))

        if len(self.getDependencies()) > 0 and self.reference.getDependencies() is None:
            self.reference.setDepEdges(java_list([e.getReference() for e in self.getDependencies()]))

        if len(self.getEntities()) > 0 and self.reference.getEntities() is None:
            self.reference.setEntities(java_list([e.getReference() for e in self.getEntities()]))

        if len(self.getCorefGroups()) > 0 and self.reference.getCorefGroups() is None:
            self.reference.setCorefGroups(java_list([e.getReference() for e in self.getCorefGroups()]))

        return self.reference

    def getSyntaxTree(self) -> SyntaxTree:
        """
        구문분석을 했다면, 최상위 구구조(Phrase)를 돌려줍니다.

        참고:
            **구문구조 분석** 은 문장의 구성요소들(어절, 구, 절)이 이루는 문법적 구조를 분석하는 방법입니다.

            예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는 2개의 절이 있습니다

            * 나는 밥을 먹었고
            * 영희는 짐을 쌌다

            각 절은 3개의 구를 포함합니다

            * 나는, 밥을, 영희는, 짐을: 체언구
            * 먹었고, 쌌다: 용언구

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.Parser` 구문구조 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getPhrase` 어절의 직속 상위 [SyntaxTree]를 가져오는 API
            * :py:class:`koalanlp.data.SyntaxTree` 구문구조를 저장하는 형태
            * :py:class:`koalanlp.types.PhraseTag` 구구조의 형태 분류를 갖는 Enum 값


        :rtype: SyntaxTree

        :return: 최상위 구구조 [SyntaxTree]. 분석 결과가 없으면 None.
        """
        return self.syntaxTree

    def getDependencies(self) -> List[DepEdge]:
        """
        의존구문분석을 했다면, 문장에 포함된 모든 의존구조의 목록을 돌려줍니다.

        참고:
            **의존구조 분석** 은 문장의 구성 어절들이 의존 또는 기능하는 관계를 분석하는 방법입니다.

            예) '나는 밥을 먹었고, 영희는 짐을 쌌다'라는 문장에는

            가장 마지막 단어인 '쌌다'가 핵심 어구가 되며,

            * '먹었고'가 '쌌다'와 대등하게 연결되고
            * '나는'은 '먹었고'의 주어로 기능하며
            * '밥을'은 '먹었고'의 목적어로 기능합니다.
            * '영희는'은 '쌌다'의 주어로 기능하고,
            * '짐을'은 '쌌다'의 목적어로 기능합니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.Parser` 의존구조 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getDependentEdges` 어절이 직접 지배하는 하위 의존구조 [DepEdge]의 목록를 가져오는 API
            * :py:meth:`koalanlp.data.Word.getGovernorEdge` 어절이 지배당하는 상위 의존구조 [DepEdge]를 가져오는 API
            * :py:meth:`koalanlp.types.PhraseTag` 의존구조의 형태 분류를 갖는 Enum 값 (구구조 분류와 같음)
            * :py:meth:`koalanlp.types.DependencyTag` 의존구조의 기능 분류를 갖는 Enum 값
            * :py:class:`koalanlp.data.DepEdge` 의존구문구조의 저장형태


        :rtype: List[DepEdge]

        :return: 문장 내 모든 의존구문구조 [DepEdge]의 목록. 분석 결과가 없으면 빈 리스트.
        """
        return self.dependencies

    def getRoles(self) -> List[RoleEdge]:
        """
        의미역 분석을 했다면, 문장에 포함된 의미역 구조의 목록을 돌려줌.

        참고:
            **의미역 결정** 은 문장의 구성 어절들의 역할/기능을 분석하는 방법입니다.

            예) '나는 밥을 어제 집에서 먹었다'라는 문장에는

            동사 '먹었다'를 중심으로

            * '나는'은 동작의 주체를,
            * '밥을'은 동작의 대상을,
            * '어제'는 동작의 시점을
            * '집에서'는 동작의 장소를 나타냅니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.RoleLabeler` 의미역 분석을 수행하는 interface.
            * :py:meth:`koalanlp.data.Word.getPredicateRoles` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
            * :py:meth:`koalanlp.data.Word.getArgumentRoles` 어절이 술어인 [RoleEdge]의 논항들을 가져오는 API
            * :py:class:`koalanlp.data.RoleEdge` 의미역 구조를 저장하는 형태
            * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값


        :rtype: List[RoleEdge]

        :return: 어절이 술어로 기능하는 하위 의미역 구조 [RoleEdge]의 목록. 분석 결과가 없으면 빈 리스트.
        """
        return self.roles

    def getEntities(self) -> List[Entity]:
        """
        개체명 분석을 했다면, 문장의 모든 개체명 목록을 돌려줍니다.

        참고:
            **개체명 인식** 은 문장에서 인물, 장소, 기관, 대상 등을 인식하는 기술입니다.

            예) '철저한 진상 조사를 촉구하는 국제사회의 목소리가 커지고 있는 가운데, 트럼프 미국 대통령은 되레 사우디를 감싸고 나섰습니다.'에서, 다음을 인식하는 기술입니다.

            * '트럼프': 인물
            * '미국' : 국가
            * '대통령' : 직위
            * '사우디' : 국가

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.EntityRecognizer` 개체명 인식기 interface
            * :py:meth:`koalanlp.data.Morpheme.getEntities` 형태소를 포함하는 모든 [Entity]를 가져오는 API
            * :py:meth:`koalanlp.data.Word.getEntities` 해당 어절을 포함하는 [Entity]를 가져오는 API
            * :py:class:`koalanlp.data.Entity` 개체명을 저장하는 형태
            * :py:class:`koalanlp.types.CoarseEntityType` [Entity]의 대분류 개체명 분류구조 Enum 값


        :rtype: List[Entity]

        :return: 문장에 포함된 모든 [Entity]의 목록입니다.
        """
        return self.entities

    def getCorefGroups(self):
        """
        문장 내에 포함된 공통 지시어 또는 대용어들의 묶음을 제공합니다.

        참고:
            **공지시어 해소** 는 문장 내 또는 문장 간에 같은 대상을 지칭하는 어구를 찾아 묶는 분석과정입니다.

            예) '삼성그룹의 계열사인 삼성물산은 같은 그룹의 계열사인 삼성생명과 함께'라는 문장에서

            * '삼성그룹'과 '같은 그룹'을 찾아 묶는 것을 말합니다.

            **영형대용어 분석** 은 문장에서 생략된 기능어를 찾아 문장 내 또는 문장 간에 언급되어 있는 어구와 묶는 분석과정입니다.

            예) '나는 밥을 먹었고, 영희도 먹었다'라는 문장에서,

            * '먹었다'의 목적어인 '밥을'이 생략되어 있음을 찾는 것을 말합니다.

            아래를 참고해보세요.

            * :py:class:`koalanlp.proc.CorefResolver` 공지시어 해소, 대용어 분석기 interface
            * :py:meth:`koalanlp.data.Sentence.getCorefGroups` 문장 내에 포함된 개체명 묶음 [CoreferenceGroup]들의 목록을 반환하는 API
            * :py:class:`koalanlp.data.CoreferenceGroup` 동일한 대상을 지칭하는 개체명을 묶는 API


        :rtype: List[CoreferenceGroup]

        :return: 공통된 대상을 묶은 [CoreferenceGroup]의 목록. 없다면 빈 리스트.
        """
        return self.corefGroups

    def getNouns(self) -> List[Word]:
        """
        체언(명사, 수사, 대명사) 및 체언 성격의 어휘를 포함하는 어절들을 가져옵니다.

        - 포함: 체언, 명사형 전성어미 [POS.ETN], 명사 파생 접미사 [POS.XSN]
        - 제외: 관형형 전성어미 [POS.ETM], 동사/형용사/부사 파생 접미사 [POS.XSV], [POS.XSA], [POS.XSM]
        - 가장 마지막에 적용되는 어미/접미사를 기준으로 판정함

        참고:
            **전성어미** 는 용언 따위에 붙어 다른 품사의 기능을 수행하도록 변경하는 어미입니다.
            예) '멋지게 살다'를 '멋지게 삶'으로 바꾸는 명사형 전성어미 '-ㅁ'이 있습니다. 원 기능은 동사이므로 부사의 수식을 받고 있습니다.

            **파생접미사** 는 용언의 어근이나 단어 따위에 붙어서 명사로 파생되도록 하는 접미사입니다.
            예) 역시 '살다'를 '삶'으로 바꾸는 명사파생 접미사 '-ㅁ'이 있습니다. 이 경우 명사이므로 '멋진 삶'과 같이 형용사의 수식을 받습니다.


        :rtype: List[Word]

        :return: 체언 또는 체언 성격의 어휘를 포함하는 어절의 목록
         """
        result = []
        for word in self:
            inclusion = -1
            exclusion = -1
            for i, m in reversed(list(enumerate(word))):
                if inclusion != -1 and (m.isNoun() or m.hasTagOneOf('ETN', 'XSN')):
                    inclusion = i
                if exclusion != -1 and m.hasTagOneOf('XSV', 'XSA', 'XSM'):
                    exclusion = i

            if inclusion != -1 and (exclusion == -1 or inclusion > exclusion):
                result.append(word)

        return result

    def getVerbs(self) -> List[Word]:
        """
        용언(동사, 형용사) 및 용언 성격의 어휘를 포함하는 어절들을 가져옵니다.

        - 포함: 용언, 동사 파생 접미사 [POS.XSV]
        - 제외: 명사형/관형형 전성어미 [POS.ETN], [POS.ETM], 명사/형용사/부사 파생 접미사 [POS.XSN], [POS.XSA], [POS.XSM]
        - 가장 마지막에 적용되는 어미/접미사를 기준으로 판정함

        참고:
            **전성어미** 는 용언 따위에 붙어 다른 품사의 기능을 수행하도록 변경하는 어미입니다.
            예) '멋지게 살다'를 '멋지게 삶'으로 바꾸는 명사형 전성어미 '-ㅁ'이 있습니다. 원 기능은 동사이므로 부사의 수식을 받고 있습니다.

            **파생접미사** 는 용언의 어근이나 단어 따위에 붙어서 명사로 파생되도록 하는 접미사입니다.
            예) 역시 '살다'를 '삶'으로 바꾸는 명사파생 접미사 '-ㅁ'이 있습니다. 이 경우 명사이므로 '멋진 삶'과 같이 형용사의 수식을 받습니다.


        :rtype: List[Word]

        :return: 용언 또는 용언 성격의 어휘를 포함하는 어절의 목록
         """
        result = []
        for word in self:
            inclusion = -1
            exclusion = -1
            for i, m in reversed(list(enumerate(word))):
                if inclusion != -1 and (m.isPredicate() or m.tag == POS.XSV):
                    inclusion = i
                if exclusion != -1 and m.hasTagOneOf("ETN", "ETM", "XSN", "XSA", "XSM"):
                    exclusion = i

            if inclusion != -1 and (exclusion == -1 or inclusion > exclusion):
                result.append(word)

        return result

    def getModifiers(self) -> List[Word]:
        """
        수식언(관형사, 부사) 및 수식언 성격의 어휘를 포함하는 어절들을 가져옵니다.

        - 포함: 수식언, 관형형 전성어미 [POS.ETM], 형용사/부사 파생 접미사 [POS.XSA], [POS.XSM]
        - 제외: 명사형 전성어미 [POS.ETN], 명사/동사 파생 접미사 [POS.XSN], [POS.XSV]
        - 가장 마지막에 적용되는 어미/접미사를 기준으로 판정함

        참고:
            **전성어미** 는 용언 따위에 붙어 다른 품사의 기능을 수행하도록 변경하는 어미입니다.
            예) '멋지게 살다'를 '멋지게 삶'으로 바꾸는 명사형 전성어미 '-ㅁ'이 있습니다. 원 기능은 동사이므로 부사의 수식을 받고 있습니다.

            **파생접미사** 는 용언의 어근이나 단어 따위에 붙어서 명사로 파생되도록 하는 접미사입니다.
            예) 역시 '살다'를 '삶'으로 바꾸는 명사파생 접미사 '-ㅁ'이 있습니다. 이 경우 명사이므로 '멋진 삶'과 같이 형용사의 수식을 받습니다.


        :rtype: List[Word]

        :return: 수식언 또는 수식언 성격의 어휘를 포함하는 어절의 목록
         """
        result = []
        for word in self:
            inclusion = -1
            exclusion = -1
            for i, m in reversed(list(enumerate(word))):
                if inclusion != -1 and (m.isPredicate() or m.hasTagOneOf("ETM", "XSA", "XSM")):
                    inclusion = i
                if exclusion != -1 and m.hasTagOneOf("ETN", "XSN", "XSV"):
                    exclusion = i

            if inclusion != -1 and (exclusion == -1 or inclusion > exclusion):
                result.append(word)

        return result

    def surfaceString(self, delimiter: str = ' ') -> str:
        """
        어절의 표면형을 이어붙이되, 지정된 [delimiter]로 띄어쓰기 된 문장을 반환합니다.

        :param str delimiter: 어절 사이의 띄어쓰기 방식. 기본값 = 공백(" ")

        :return: 띄어쓰기 된 문장입니다.
        """
        return delimiter.join(word.surface for word in self)

    def singleLineString(self) -> str:
        """
        품사분석 결과를, 1행짜리 String으로 변환합니다.


        :rtype: str

        :return: 품사분석 결과를 담은 1행짜리 String.
        """
        return ' '.join(word.singleLineString() for word in self)

    def __repr__(self) -> str:
        """
        문자열 표현을 생성합니다.

        :rtype: str
        :return: 이 객체의 문자열 표현
        """
        return self.surfaceString()

    @staticmethod
    def fromJava(ref):
        return Sentence(reference=ref)


# ----- define members exported -----

__all__ = ['Entity', 'CoreferenceGroup', 'SyntaxTree', 'DepEdge', 'RoleEdge', 'Morpheme', 'Word', 'Sentence']
