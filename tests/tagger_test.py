from koalanlp import *
from koalanlp.types import *
from koalanlp.data import *
from koalanlp.proc import *
import pytest

Util.initialize([API.EUNJEON], "2.0.0")
tagger = Tagger(API.EUNJEON)

def test_tag_sentence():
    result = tagger.tagSentence("안녕하세요.")
    assert not type(result) is list
    assert type(result) is Sentence
    assert len(result) == 2
    assert result.surfaceString() == "안녕하세요 ."
    assert result[0].getSurface() == "안녕하세요"
    assert len(result[0]) == 4
    assert result[0][0].getSurface() == "안녕"

    result = tagger.tagSentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert not type(result) is list
    assert len(result) == 7

def test_tag():
    result = tagger.tag("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert type(result) is list
    assert len(result) == 2
    assert len(result[0]) == 2
    assert type(result[0]) is Sentence
    assert result[0].surfaceString() == "안녕하세요 ."
    assert result[0][0].getSurface() == "안녕하세요"
    assert len(result[1]) == 5
    assert result[1].surfaceString() == "눈이 오는 설날 아침입니다 ."
    assert result[1][0].getSurface() == "눈이"
    assert result[1][0][0].getSurface() == "눈"
    assert result[1][0][0].getTag().name() == "NNG"
    assert result[1][0][0].getOriginalTag() == "NNG"
    assert result[1][0][1].getSurface() == "이"
    assert result[1][0][1].getOriginalTag() == "JKS"
    assert result[1][3].getSurface() == "아침입니다"
    assert result[1][3][2].getSurface() == "ᄇ니다"
    assert result[1][3][2].getTag().name() == "EF"
