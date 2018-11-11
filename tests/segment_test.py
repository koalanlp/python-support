from koalanlp import *
from koalanlp.types import *
from koalanlp.data import *
from koalanlp.proc import *
import pytest

Util.initialize([API.OKT, API.EUNJEON], "2.0.0")
tagger = Tagger(API.EUNJEON)
segmenter = SentenceSplitter(API.OKT)


def test_sentences():
    result = segmenter.sentences("안녕하세요.")
    assert type(result) is list
    assert type(result[0]) is str
    assert len(result) == 1
    assert result[0] == "안녕하세요."

    result = segmenter.sentences("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert len(result) == 2
    assert result[0] == "안녕하세요."
    assert result[1] == "눈이 오는 설날 아침입니다."


def test_sentence_by_koala():
    result = tagger.tagSentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    result = SentenceSplitter.sentencesTagged(result)
    assert len(result) == 2
    assert len(result[0]) == 2
    assert result[0].surfaceString() == "안녕하세요 ."
    assert result[0][0].getSurface() == "안녕하세요"
    assert len(result[1]) == 5
    assert result[1].surfaceString() == "눈이 오는 설날 아침입니다 ."
    assert result[1][0].getSurface()== "눈이"
    assert result[1][0][0].getSurface() == "눈"
    assert result[1][0][0].getTag().name() == "NNG"
    assert result[1][0][0].getOriginalTag() == "NNG"
    assert result[1][0][1].getSurface() == "이"
    assert result[1][0][1].getOriginalTag() == "JKS"
    assert result[1][3].getSurface() == "아침입니다"
    assert result[1][3][2].getSurface() == "ᄇ니다"
    assert result[1][3][2].getTag().name() == "EF"
