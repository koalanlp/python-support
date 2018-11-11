#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .types import *
from .jnius import *
from typing import Union, List


def _get_item_(jlist, item, item_converter=lambda x: x):
    if type(item) is tuple:
        result = []
        for index in item:
            res = _get_item_(jlist, index, item_converter)
            if type(res) is list:
                result += res
            else:
                result.append(res)
        return result
    elif type(item) is slice:
        return [item_converter(jlist.get(index)) for index in range(*item.indicies(jlist.size()))]
    elif type(item) is int:
        return item_converter(jlist.get(item))
    else:
        raise Exception("%s is not supported!" % item.__class__)


class _JavaDataWrap(object):
    def __init__(self, reference):
        self.reference = reference

    def __repr__(self) -> str:
        """
        문자열 표현을 생성합니다.

        :rtype: str
        :return: 이 객체의 문자열 표현
        """
        return self.reference.toString()

    def __eq__(self, other) -> bool:
        """
        두 대상이 같은지 확인합니다.

        :param other: 이 객체와 비교할 다른 객체
        :rtype: bool
        :return: Java Reference가 같다면 true.
        """
        return type(other) is type(self) and other.reference.equals(self.reference)

    def __hash__(self) -> int:
        """
        해쉬 값을 계산합니다.

        :rtype: int
        :return: Java Reference의 Hash code
        """
        return self.reference.hashcode()


class Entity(_JavaDataWrap):
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

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 개체명의 표면형 문자열.
        """
        return self.reference.getSurface()

    def getLabel(self) -> CoarseEntityType:
        """
        :rtype: CoarseEntityType

        :return: 개체명 대분류 값, [CoarseEntityType]에 기록된 개체명 중 하나.
        """
        return CoarseEntityType.valueOf(self.reference.getLabel().name())

    def getFineLabel(self) -> str:
        """
        :rtype: str

        :return: 개체명 세분류 값으로, [label]으로 시작하는 문자열.
        """
        return self.reference.getFineLabel()

    def getOriginalLabel(self) -> Union[str, None]:
        """
        :rtype: str 또는 None

        :return: 원본 분석기가 제시한 개체명 분류의 값. 기본값은 null.
        """
        return self.reference.getOriginalLabel()

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
        obj = self.reference.getCorefGroup()
        return CoreferenceGroup(obj) if obj is not None else None

    def __getitem__(self, item):
        """
        포함된 형태소를 가져옵니다.

        :param item: index의 번호 또는 slice
        :rtype: List[Morpheme]
        :return: 지정된 위치에 있는 형태소(들)
        """
        return _get_item_(self.reference, item, lambda x: Morpheme(x))

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 형태소를 순회하는 iterator
        """
        return iter(py_list(self.reference, lambda x: Morpheme(x)))

    def __contains__(self, item) -> bool:
        """
        형태소가 포함되는지 확인합니다.

        :param Morpheme item: 포함되는지 확인할 형태소
        :rtype: bool
        :return: 해당 형태소가 포함되면 true.
        """
        return type(item) is Morpheme and self.reference.contains(item.reference)

    def __len__(self):
        """
        :rtype: int
        :return: 포함된 형태소의 개수
        """
        return self.reference.size()


class CoreferenceGroup(_JavaDataWrap):
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

    def __getitem__(self, item):
        """
        포함된 개체명을 가져옵니다.

        :param item: index의 번호 또는 slice
        :rtype: List[Entity]
        :return: 지정된 위치에 있는 개체명(들)
        """
        return _get_item_(self.reference, item, lambda x: Entity(x))

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 개체명을 순회하는 iterator
        """
        return iter(py_list(self.reference, lambda x: Entity(x)))

    def __contains__(self, item) -> bool:
        """
        개체명이 포함되는지 확인합니다.

        :param Entity item: 포함되는지 확인할 개체명
        :rtype: bool
        :return: 해당 개체명이 포함되면 true.
        """
        return type(item) is Entity and self.reference.contains(item.reference)

    def __len__(self):
        """
        :rtype: int
        :return: 포함된 개체명의 개수
        """
        return self.reference.size()


class Tree(_JavaDataWrap):
    """
    트리 구조를 저장할 [Property]입니다. :py:class:`Word`를 묶어서 표현하는 구조에 적용됩니다.
    """

    def __contains__(self, item) -> bool:
        """
        트리 구조가 포함되는지 확인합니다.

        :param Tree item: 포함되는지 확인할 트리 구조
        :rtype: bool
        :return: 해당 구조가 포함되면 true.
        """
        return type(item) is Tree and self.reference.contains(item.reference)

    def __len__(self):
        """
        :rtype: int
        :return: 포함된 하위 구조의 개수
        """
        return self.reference.size()

    def _getLabel(self, cls):
        """
        트리에 붙어있는 표지자입니다. Null일 수 없습니다.

        :param cls: 표지자를 cast할 class

        :return: cast된 표지자
        """
        return cls.valueOf(self.reference.getLabel().name())

    def getTerminal(self):
        """

        :rtype: Word 또는 None

        :return: 트리의 노드에서 연결되는 [Word] 
        """
        obj = self.reference.getTerminal()
        return Word(obj) if obj is not None else None

    def isRoot(self) -> bool:
        """
        이 노드가 최상위 노드인지 확인합니다.

        :rtype: bool

        :return: 최상위 노드인 경우 true
        """
        return self.reference.isRoot()

    def hasNonTerminal(self) -> bool:
        """
        이 노드가 (terminal node를 제외하고) 자식 노드를 갖는지 확인합니다.

        * 구문분석 구조에서 terminal node는 [Word]가 됩니다.

        :rtype: bool

        :return: 자식노드가 있다면 True
        """
        return self.reference.hasNonTerminal()

    def getTerminals(self):
        """
        이 노드를 포함해 모든 하위 Non-terminal 노드들에 속하는 terminal node들을 모읍니다.

        * 구문분석 구조에서는 이 구문구조에 속하는 어절의 모음입니다.


        :rtype: List[Word]

        :return: Terminal node의 목록
        """
        return py_list(self.reference.getTerminals(), lambda x: Word(x))

    def getTreeString(self) -> str:
        """
        이 트리구조를 표현하는 텍스트 표현을 [buffer]에 담아 반환합니다.


        :return: 트리구조의 표현을 문자열로 돌려줍니다.
        """
        return self.reference.getTreeString().toString()

    def _getParent(self, cls):
        """
        부모 노드를 반환합니다.

        * 부모 노드가 초기화되지 않은 경우 null을 반환합니다.


        :param cls: Casting할 Python Class

        :return: 같은 타입의 부모 노드 또는 null
        """
        obj = self.reference.getParent()
        return cls(obj) if obj is not None else None

    def _getNonTerminals(self, cls):
        """
        이 노드의 Non-terminal 자식 노드를 모읍니다.

        * 이 함수는 읽기의 편의를 위한 syntactic sugar입니다. 즉 다음 구문은 동일합니다.

        .. code-block:: python

            for item in x.getNonTerminals():
                ...
            for item in x:
                ...


        :param cls: Casting할 Python Class

        :return: 같은 타입의 부모 노드 또는 null
        """
        return py_list(self.reference, lambda x: cls(x))


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

    def __getitem__(self, item):
        """
        하위 구문구조를 가져옵니다.

        :param item: index의 번호 또는 slice
        :rtype: List[SyntaxTree]
        :return: 지정된 위치에 있는 구문구조(들)
        """
        return _get_item_(self.reference, item, lambda x: SyntaxTree(x))

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 하위 구문구조를 순회하는 iterator
        """
        return iter(py_list(self.reference, lambda x: SyntaxTree(x)))

    def getLabel(self) -> PhraseTag:
        """

        :rtype: PhraseTag

        :return: 구구조 표지자입니다. [PhraseTag] Enum 값입니다.
        """
        return super()._getLabel(PhraseTag)

    def getOriginalLabel(self) -> Union[str, None]:
        """

        :rtype: str 또는 None

        :return: 원본 분석기의 표지자 String 값. 기본값은 None.
        """
        return self.reference.getOriginalLabel()

    def getParent(self):
        """
        부모 노드를 반환합니다.

        * 부모 노드가 초기화되지 않은 경우 None을 반환합니다.


        :rtype: SyntaxTree 또는 None

        :return: 같은 타입의 부모 노드 또는 None
        """
        return super()._getParent(SyntaxTree)

    def getNonTerminals(self) -> List:
        """
        이 노드의 Non-terminal 자식 노드를 모읍니다.

        * 이 함수는 읽기의 편의를 위한 syntactic sugar입니다. 즉 다음 구문은 동일합니다.

        .. code-block:: python

            for item in x.getNonTerminals():
                ...
            for item in x:
                ...

        :rtype: List[SyntaxTree]

        :return: 같은 타입의 부모 노드 또는 null
        """
        return super()._getNonTerminals(SyntaxTree)


class DAGEdge(_JavaDataWrap):
    """
    DAG Edge를 저장합니다.
    """

    def _getSrc(self, cls):
        """
        Edge의 시작점. 의존구문분석인 경우 지배소, 의미역인 경우 동사.

        :param cls: Casting할 class

        :return: casting된 src
        """
        obj = self.reference.getSrc()
        return cls(obj) if obj is not None else None

    def _getDest(self, cls):
        """
        Edge의 종점. 의존구문분석인 경우 피지배소, 의미역인 경우 논항.

        :param cls: Casting할 class

        :return: casting된 dest
        """
        obj = self.reference.getDest()
        return cls(obj) if obj is not None else None

    def _getLabel(self, cls):
        """
        Edge가 나타내는 관계.

        :param cls: Casting할 class

        :return: casting된 label
        """
        obj = self.reference.getLabel()
        return cls.valueOf(obj.name()) if obj is not None else None


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

    def getSrc(self):
        """

        :rtype: Word 또는 None

        :return: 의존구조의 지배소 [Word]. 문장의 Root에 해당하는 경우 None.
        """
        return super()._getSrc(Word)

    def getGovernor(self):
        """

        :rtype: Word 또는 None

        :return: 의존구조의 지배소 [Word]. 문장의 Root에 해당하는 경우 None.
        """
        return self.getSrc()

    def getDest(self):
        """

        :rtype: Word

        :return: 의존구조의 피지배소 [Word]
        """
        return super()._getDest(Word)

    def getDependent(self):
        """

        :rtype: Word

        :return: 의존구조의 피지배소 [Word]
        """
        return self.getDest()

    def getLabel(self) -> Union[DependencyTag, None]:
        """

        :rtype: DependencyTag 또는 None

        :return: 의존기능 표지자, [DependencyTag] Enum 값. 별도의 기능이 지정되지 않으면 null. (ETRI 표준안은 구구조+의존기능으로 의존구문구조를 표기함)
        """
        return super()._getLabel(DependencyTag)

    def getDepType(self) -> Union[DependencyTag, None]:
        """

        :rtype: DependencyTag 또는 None

        :return: 의존기능 표지자, [DependencyTag] Enum 값. 별도의 기능이 지정되지 않으면 null. (ETRI 표준안은 구구조+의존기능으로 의존구문구조를 표기함)
        """
        return self.getLabel()

    def getType(self) -> PhraseTag:
        """

        :rtype: PhraseTag

        :return: 구구조 표지자, [PhraseTag] Enum 값 (ETRI 표준안은 구구조+의존기능으로 의존구문구조를 표기함)
        """
        obj = self.reference.getType()
        return PhraseTag.valueOf(obj.name()) if obj is not None else None

    def getOriginalLabel(self) -> Union[str, None]:
        """

        :rtype: str 또는 None

        :return: 원본 분석기의 표지자 String 값. 기본값은 null.
        """
        return self.reference.getOriginalLabel()


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
        * :py:meth:`koalanlp.data.Word.getPredicateRole` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
        * :py:meth:`koalanlp.data.Sentence.getRoles` 전체 문장을 분석한 의미역 구조 [RoleEdge]를 가져오는 API
        * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값
    """

    def getSrc(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 표현하는 동사 [Word]
        """
        return super()._getSrc(Word)

    def getPredicate(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 표현하는 동사 [Word]
        """
        return self.getSrc()

    def getDest(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 서술된 논항 [Word]
        """
        return super()._getDest(Word)

    def getArgument(self):
        """

        :rtype: Word

        :return: 의미역 구조에서 서술된 논항 [Word]
        """
        return self.getDest()

    def getLabel(self) -> RoleType:
        """

        :rtype: RoleType

        :return: 의미역 표지자, [RoleType] Enum 값
        """
        return super()._getLabel(RoleType)

    def getModifiers(self) -> List:
        """

        :rtype: List[Word]

        :return: 논항의 수식어구들
        """
        return py_list(self.reference.getModifiers(), lambda x: Word(x))

    def getOriginalLabel(self) -> Union[str, None]:
        """

        :rtype: str 또는 None

        :return: 원본 분석기의 표지자 String 값. 기본값은 null.
        """
        return self.reference.getOriginalLabel()


class Morpheme(_JavaDataWrap):
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

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 형태소 표면형 String
        """
        return self.reference.getSurface()

    def getOriginalTag(self) -> Union[str, None]:
        """

        :rtype: str 또는 None

        :return: 원본 형태소 분석기의 품사 String
        """
        return self.reference.getOriginalTag()

    def getTag(self) -> POS:
        """

        :rtype: POS

        :return: 세종 품사표기
        """
        return POS.valueOf(self.reference.getTag().name())

    def getId(self) -> int:
        """

        :rtype: int

        :return: 형태소의 어절 내 위치입니다.
        """
        return self.reference.getId()

    def getWordSense(self) -> Union[int, None]:
        """
        다의어 분석 결과인, 이 형태소의 사전 속 의미/어깨번호 값을 돌려줍니다.

        다의어 분석을 한 적이 없다면 None을 돌려줍니다.


        :rtype: int 또는 None

        :return: 의미/어깨번호 값
        """
        return self.reference.getWordSense()

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

        :return: [Entity]의 목록입니다. 분석 결과가 없으면 빈 리스트.
        """

        return py_list(self.reference.getEntities(), lambda x: Entity(x))

    def getWord(self):
        """

        :rtype: Word

        :return: 이 형태소를 포함하는 단어를 돌려줍니다. 
        """
        return Word(self.reference.getWord())

    def isNoun(self) -> bool:
        """
        체언(명사, 수사, 대명사) 형태소인지 확인합니다.        

        :rtype: bool

        :return: 체언이라면 true
        """

        return self.reference.isNoun()

    def isPredicate(self) -> bool:
        """
        용언(동사, 형용사) 형태소인지 확인합니다.        

        :rtype: bool

        :return: 용언이라면 true
        """

        return self.reference.isPredicate()

    def isModifier(self) -> bool:
        """
        수식언(관형사, 부사) 형태소인지 확인합니다.        

        :rtype: bool

        :return: 수식언이라면 true
        """

        return self.reference.isModifier()

    def isJosa(self) -> bool:
        """
        관계언(조사) 형태소인지 확인합니다.        

        :rtype: bool

        :return: 관계언이라면 true
        """

        return self.reference.isJosa()

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
        return self.reference.hasTag(string(partialTag))

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
        return self.reference.hasTagOneOf([string(t) for t in tags])

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
        return self.reference.hasOriginalTag(string(partialTag))

    def equalsWithoutTag(self, other):
        """
        타 형태소 객체 [another]와 형태소의 표면형이 같은지 비교합니다.

        :param Morpheme other: 표면형을 비교할 형태소

        :rtype: bool

        :return: 표면형이 같으면 True
        """
        return self.reference.equalsWithoutTag(other.reference)


class Word(_JavaDataWrap):
    """
    어절을 표현하는 [Property] class입니다.
    """

    def __getitem__(self, item):
        """
        포함된 형태소를 가져옵니다.

        :param item: index의 번호 또는 slice
        :rtype: List[Morpheme]
        :return: 지정된 위치에 있는 형태소(들)
        """
        return _get_item_(self.reference, item, lambda x: Morpheme(x))

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 형태소를 순회하는 iterator
        """
        return iter(py_list(self.reference, lambda x: Morpheme(x)))

    def __contains__(self, item) -> bool:
        """
        형태소가 포함되는지 확인합니다.

        :param Morpheme item: 포함되는지 확인할 형태소
        :rtype: bool
        :return: 해당 형태소가 포함되면 true.
        """
        return type(item) is Morpheme and self.reference.contains(item.reference)

    def __len__(self):
        """
        :rtype: int
        :return: 포함된 형태소의 개수
        """
        return self.reference.size()

    def getSurface(self) -> str:
        """

        :rtype: str

        :return: 어절의 표면형 String.
        """
        return self.reference.getSurface()

    def getId(self) -> int:
        """

        :rtype: int

        :return: 어절의 문장 내 위치입니다.
        """
        return self.reference.getId()

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
        return py_list(self.reference.getEntities(), lambda x: Entity(x))

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
        obj = self.reference.getPhrase()
        return SyntaxTree(obj) if obj is not None else None

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

        :return: 어절이 지배하는 의존구문구조 [DepEdge]의 목록. 분석 결과가 없으면 빈 리스트
        """
        return py_list(self.reference.getDependentEdges(), lambda x: DepEdge(x))

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
        obj = self.reference.getGovernorEdge()
        return DepEdge(obj) if obj is not None else None

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
            * :py:meth:`koalanlp.data.Word.getPredicateRole` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
            * :py:meth:`koalanlp.data.Sentence.getRoles` 전체 문장을 분석한 의미역 구조 [RoleEdge]를 가져오는 API
            * :py:class:`koalanlp.data.RoleEdge` 의미역 구조를 저장하는 형태
            * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값


        :rtype: List[RoleEdge]

        :return: 어절이 술어로 기능하는 하위 의미역 구조 [RoleEdge]의 목록. 분석 결과가 없으면 null.
        """
        return py_list(self.reference.getArgumentRoles(), lambda x: RoleEdge(x))

    def getPredicateRole(self) -> RoleEdge:
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

        :return: 어절이 논항인 상위 의미역 구조 [RoleEdge]. 분석 결과가 없으면 null.
        """
        obj = self.reference.getPredicateRole()
        return RoleEdge(obj) if obj is not None else None

    def singleLineString(self) -> str:
        """
        품사분석 결과를, 1행짜리 String으로 변환합니다.

        예) '나/NP+는/JX'

        참고:
            * 세종 품사표기는 :py:class:`koalanlp.types.POS` 를 참고하세요.


        :return: 각 형태소별로 "표면형/품사" 형태로 기록하고 이를 +로 이어붙인 문자열.
        """
        return self.reference.singleLineString()


class Sentence(_JavaDataWrap):
    """
    문장을 표현하는 [Property] class입니다.
    """
    def __getitem__(self, item):
        """
        포함된 어절을 가져옵니다.

        :param item: index의 번호 또는 slice
        :rtype: List[Word]
        :return: 지정된 위치에 있는 어절(들)
        """
        return _get_item_(self.reference, item, lambda x: Morpheme(x))

    def __iter__(self):
        """
        :rtype: iter
        :return: 포함된 어절을 순회하는 iterator
        """
        return iter(py_list(self.reference, lambda x: Morpheme(x)))

    def __contains__(self, item) -> bool:
        """
        어절이 포함되는지 확인합니다.

        :param Word item: 포함되는지 확인할 어절
        :rtype: bool
        :return: 해당 어절이 포함되면 true.
        """
        return type(item) is Morpheme and self.reference.contains(item.reference)

    def __len__(self):
        """
        :rtype: int
        :return: 문장 속 어절의 개수
        """
        return self.reference.size()

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

        :return: 최상위 구구조 [SyntaxTree]. 분석 결과가 없으면 null.
        """
        obj = self.reference.getSyntaxTree()
        return SyntaxTree(obj) if obj is not None else None

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

        :return: 문장 내 모든 의존구문구조 [DepEdge]의 목록. 분석 결과가 없으면 null.
        """
        return py_list(self.reference.getDependencies(), lambda x: DepEdge(x))

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
            * :py:meth:`koalanlp.data.Word.getPredicateRole` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
            * :py:meth:`koalanlp.data.Word.getPredicateRole` 어절이 논항인 [RoleEdge]의 술어를 가져오는 API
            * :py:class:`koalanlp.data.RoleEdge` 의미역 구조를 저장하는 형태
            * :py:class:`koalanlp.types.RoleType` 의미역 분류를 갖는 Enum 값


        :rtype: List[RoleEdge]

        :return: 어절이 술어로 기능하는 하위 의미역 구조 [RoleEdge]의 목록. 분석 결과가 없으면 null.
        """
        return py_list(self.reference.getRoles(), lambda x: RoleEdge(x))

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
        return py_list(self.reference.getEntities(), lambda x: Entity(x))

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
        return py_list(self.reference.getCorefGroups(), lambda x: CoreferenceGroup(x))

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

        return py_list(self.reference.getNouns(), lambda x: Word(x))

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

        :return: 체언 또는 체언 성격의 어휘를 포함하는 어절의 목록
         """

        return py_list(self.reference.getVerbs(), lambda x: Word(x))

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

        :return: 체언 또는 체언 성격의 어휘를 포함하는 어절의 목록
         """

        return py_list(self.reference.getModifiers(), lambda x: Word(x))

    def surfaceString(self, delimiter: str = ' ') -> str:
        """
        어절의 표면형을 이어붙이되, 지정된 [delimiter]로 띄어쓰기 된 문장을 반환합니다.

        :param str delimiter: 어절 사이의 띄어쓰기 방식. 기본값 = 공백(" ")

        :return: 띄어쓰기 된 문장입니다.
        """

        return self.reference.surfaceString(string(delimiter))

    def singleLineString(self) -> str:
        """
        품사분석 결과를, 1행짜리 String으로 변환합니다.


        :rtype: str

        :return: 품사분석 결과를 담은 1행짜리 String.
        """

        return self.reference.singleLineString()


# ----- define members exported -----

__all__ = ['Entity', 'CoreferenceGroup', 'SyntaxTree', 'DepEdge', 'RoleEdge', 'Morpheme', 'Word', 'Sentence']
