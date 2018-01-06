#!/usr/bin/env python
# -*- coding: utf-8 -*-

from koalanlp.data import *
from .const import API
from typing import List


def _convert_word(result, widx) -> Word:
    w_length = result.length()
    morphemes = []
    surface = result.surface()

    for i in range(w_length):
        morphs = result.apply(i)
        morpheme = Morpheme(morphs.surface(),
                            morphs.tag().toString(),
                            morphs.rawTag(),
                            i)
        morphemes.append(morpheme)

    word = Word(surface, morphemes, widx)
    dependents = result.deps().toSeq()
    d_length = dependents.size()

    for i in range(d_length):
        rel = dependents.apply(i)
        relationship = Relationship(rel.head(),
                                    rel.relation().toString(),
                                    rel.rawRel(),
                                    rel.target())
        word.dependents.append(relationship)

    return word


def _convert_sentence(result) -> Sentence:
    s_length = result.length()
    words = []

    for i in range(s_length):
        word = result.apply(i)
        words.append(_convert_word(word, i))

    sentence = Sentence(words, result)
    dependents = result.root().deps().toSeq()
    d_length = dependents.size()

    for i in range(d_length):
        rel = dependents.apply(i)
        relationship = Relationship(rel.head(),
                                    rel.relation().toString(),
                                    rel.rawRel(),
                                    rel.target())
        sentence.root.dependents.append(relationship)

    return sentence


def _converter(result) -> List[Sentence]:
    p_length = result.size()
    para = []

    for i in range(p_length):
        sentence = result.apply(i)
        para.append(_convert_sentence(sentence))

    return para


def _convert_sentence_str(result) -> List[str]:
    p_length = result.size()
    para = []

    for i in range(p_length):
        sentence = result.apply(i)
        para.append(sentence)

    return para


JString = None


def _jstr(s):
    global JString
    if JString is None:
        from jnius import autoclass
        JString = autoclass('java.lang.String')
    return JString(s.encode("UTF-8"))


def sentenceSplitByKoala(paragraph: Sentence) -> List[Sentence]:
    """
    KoalaNLP가 구현한 문장분리기를 사용하여, 문단을 문장으로 분리합니다.

    :param Sentence paragraph: 분석할 문단. (품사표기가 되어있어야 합니다)
    :return List[Sentence]: 분리된 문장
    """
    from jnius import autoclass
    Splitter = autoclass("kr.bydelta.koala.util.SentenceSplitter")
    return _converter(Splitter.apply(paragraph.reference))


class Tagger(object):
    """
    품사분석기를 초기화합니다.

    :param API tagger_type: 사용할 품사분석기의 유형.
    """
    def __init__(self, tagger_type: API):
        from jnius import autoclass
        JTagger = autoclass("kr.bydelta.koala.%s.Tagger" % tagger_type.value)
        self.__tag = JTagger()

    def tag(self, paragraph: str) -> List[Sentence]:
        """
        문단을 품사분석합니다.

        :param str paragraph: 분석할 문단.
        :return List[Sentence]: 분석된 결과.
        """
        return _converter(self.__tag.tag(_jstr(paragraph)))

    def tag_sentence(self, sentence: str) -> Sentence:
        """
        문장을 의존구문분석합니다.

        :param str sentence: 분석할 문단.
        :return Sentence: 분석된 결과.
        """
        return _convert_sentence(self.__tag.tagSentence(_jstr(sentence)))


class Parser(object):
    """
    의존구문분석기를 초기화합니다.

    :param API parser_type: 사용할 의존구문분석기의 유형.
    :param API tagger_type: 사용할 품사분석기의 유형. 지정하지 않을 경우, 의존구문분석기의 품사분석결과를 활용함.
    """

    def __init__(self, parser_type: API, tagger_type=None):
        assert parser_type == API.KKMA or parser_type == API.HANNANUM
        from jnius import autoclass
        JParser = autoclass("kr.bydelta.koala.%s.Parser" % parser_type.value)
        self.__parse = JParser()
        if not(tagger_type is None):
            JTagger = autoclass("kr.bydelta.koala.%s.Tagger" % tagger_type.value)
            self.__tag = JTagger()
        else:
            self.__tag = None

    def parse(self, paragraph) -> List[Sentence]:
        """
        문단을 의존구문분석합니다.

        :param Union[str,List[Sentence]] paragraph: 분석할 문단.
        :return List[Sentence]: 분석된 결과.
        """
        is_sentences = type(paragraph) is list and type(paragraph[0]) is Sentence
        if self.__tag is None or is_sentences:
            if is_sentences:
                target = [sent.reference for sent in paragraph]
            else:
                target = _jstr(paragraph)
            return _converter(self.__parse.parse(target))
        else:
            tagged = self.__tag.tag(_jstr(paragraph))
            return _converter(self.__parse.parse(tagged))

    def parse_sentence(self, sentence) -> Sentence:
        """
        문장을 의존구문분석합니다.

        :param Union[str,Sentence] sentence: 분석할 문단.
        :return Sentence: 분석된 결과.
        """
        is_sentence = type(sentence) is Sentence
        if self.__tag is None or is_sentence:
            if is_sentence:
                target = sentence.reference
            else:
                target = _jstr(sentence)
            return _convert_sentence(self.__parse.parse(target))
        else:
            tagged = self.__tag.tagSentence(_jstr(sentence))
            return _convert_sentence(self.__parse.parse(tagged))


class SentenceSplitter(object):
    """
    문장분리기를 생성합니다.

    :param API splitter_type: 문장분리기 API 패키지.
    """
    def __init__(self, splitter_type):
        assert splitter_type == API.TWITTER or splitter_type == API.HANNANUM
        from jnius import autoclass
        JSeg = autoclass("kr.bydelta.koala.%s.SentenceSplitter" % splitter_type.value)
        self.__seg = JSeg()

    def sentences(self, paragraph: str) -> List[str]:
        """
        문단을 문장으로 분리합니다.

        :param str paragraph: 분석할 문단.
        :return List[str]: 분리한 문장들.
        """
        parsed = self.__seg.sentences(_jstr(paragraph))
        return _convert_sentence_str(parsed)


class Dictionary(object):
    """
    사용자 정의 사전을 연결합니다.

    :param API dic_type: 사용자 정의 사전을 연결할 API 패키지.
    """
    def __init__(self, dic_type: API):
        assert dic_type != API.RHINO
        from jnius import autoclass
        JDict = autoclass("kr.bydelta.koala.%s.JavaDictionary" % dic_type.value)
        self.__dictionary = JDict.get()
        self.__autoclass = autoclass

    def add_user_dictionary(self, morph: str, tag: str):
        """
        사용자 사전에, 표면형과 그 품사를 추가.

        :param Union[str,List[str]] morph: 표면형.
        :param Union[str,List[str]] tag: 세종 품사.
        """
        is_m_array = type(morph) is list
        is_t_array = type(tag) is list

        assert is_m_array == is_t_array
        POS = self.__autoclass('kr.bydelta.koala.POS')

        if is_m_array:
            assert len(morph) == len(tag)
            Tuple2 = self.__autoclass('scala.Tuple2')
            Predef = self.__autoclass('scala.Predef')

            zipped = [Tuple2(_jstr(m), POS.withName(_jstr(t))) for (m, t) in zip(morph, tag)]
            zipped = Predef.genericArrayOps(zipped).toSeq()

            self.__dictionary.addUserDictionary(zipped)
        else:
            self.__dictionary.addUserDictionary(_jstr(morph), POS.withName(_jstr(tag)))

    def contains(self, word: str, *pos_tags: str) -> bool:
        """
        사전에 등재되어 있는지 확인합니다.

        :param str word: 확인할 형태소
        :param str pos_tags: 세종품사들(기본값: NNP 고유명사, NNG 일반명사)
        :return:
        """
        if len(pos_tags) > 0:
            tags = pos_tags
        else:
            tags = ["NNP", "NNG"]
        POS = self.__autoclass('kr.bydelta.koala.POS')
        tags = [POS.withName(_jstr(t)) for t in tags]
        Predef = self.__autoclass('scala.Predef')
        pos_set = Predef.genericArrayOps(tags).toSet()

        return self.__dictionary.contains(_jstr(word), pos_set)

    def get_not_exists(self, only_system_dic: bool, *word):
        """
        사전에 등재되어 있는지 확인하고, 사전에 없는단어만 반환합니다.

        :param bool only_system_dic: 시스템 사전에서만 검색할지 결정합니다.
        :param List[(str,str)] word: 확인할 (형태소, 품사)들.
        :return List[(str,str)]: 사전에 없는 단어들.
        """
        POS = self.__autoclass('kr.bydelta.koala.POS')
        Tuple2 = self.__autoclass('scala.Tuple2')
        Predef = self.__autoclass('scala.Predef')

        zipped = [Tuple2(_jstr(m), POS.withName(_jstr(t))) for (m, t) in word]
        zipped = Predef.genericArrayOps(zipped).toSeq()

        not_exists = self.__dictionary.getNotExists(only_system_dic, zipped)
        not_exists = [not_exists.apply(i) for i in range(not_exists.size())]
        return [(m._1, m._2.toString()) for m in not_exists]
