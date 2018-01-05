#!/usr/bin/env python
# -*- coding: utf-8 -*-

from koalanlp.data import *
from .const import API
from typing import List


def _convert_word(result, widx):
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


def _convert_sentence(result):
    s_length = result.length()
    words = []

    for i in range(s_length):
        word = result.apply(i)
        words.append(_convert_word(word, i))

    sentence = Sentence(words)
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


def _converter(result):
    p_length = result.size()
    para = []

    for i in range(p_length):
        sentence = result.apply(i)
        para.append(_convert_sentence(sentence))

    return para


JString = None


def _jstr(s):
    global JString
    if JString is None:
        from jnius import autoclass
        JString = autoclass('java.lang.String')
    return JString(s.encode("UTF-8"))


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
        from jnius import autoclass
        JParser = autoclass("kr.bydelta.koala.%s.Parser" % parser_type.value)
        self.__parse = JParser()
        if not(tagger_type is None):
            JTagger = autoclass("kr.bydelta.koala.%s.Tagger" % tagger_type.value)
            self.__tag = JTagger()
        else:
            self.__tag = None

    def parse(self, paragraph: str) -> List[Sentence]:
        """
        문단을 의존구문분석합니다.

        :param str paragraph: 분석할 문단.
        :return List[Sentence]: 분석된 결과.
        """
        if self.__tag is None:
            return _converter(self.__parse.parse(_jstr(paragraph)))
        else:
            tagged = self.__tag.tag(_jstr(paragraph))
            return _converter(self.__parse.parse(tagged))

    def parse_sentence(self, sentence: str) -> Sentence:
        """
        문장을 의존구문분석합니다.

        :param str sentence: 분석할 문단.
        :return Sentence: 분석된 결과.
        """
        if self.__tag is None:
            return _convert_sentence(self.__parse.parseSentence(_jstr(sentence)))
        else:
            tagged = self.__tag.tagSentence(_jstr(sentence))
            return _convert_sentence(self.__parse.parse(tagged))
