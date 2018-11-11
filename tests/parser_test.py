from koalanlp import *
from koalanlp.types import *
from koalanlp.data import *
from koalanlp.proc import *
import pytest

Util.initialize([API.EUNJEON, API.KKMA], "2.0.0")
parser = Parser(API.KKMA)
tagger = Tagger(API.EUNJEON)


def test_parse():
    result = parser.analyze("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert len(result) == 2
    assert len(result[0]) == 1
    assert type(result[0]) is Sentence
    assert result[0].surfaceString() == "안녕하세요."  # KKMA
    assert result[0][0].getSurface() == "안녕하세요."
    assert len(result[1]) == 4
    assert len(result[1].getDependencies()) > 0
    assert result[1].surfaceString() == "눈이 오는 설날 아침입니다."  # KKMA
    assert result[1][0].getSurface() == "눈이"
    assert result[1][0][0].getSurface() == "눈"
    assert result[1][0][0].getTag().name() == "NNG"
    assert result[1][0][0].getOriginalTag() == "NNG"
    assert result[1][0][1].getSurface() == "이"
    assert result[1][0][1].getOriginalTag() == "JKS"
    assert result[1][3].getSurface() == "아침입니다."
    assert result[1][3][2].getSurface() == "ㅂ니다"  # KKMA (받침아님)
    assert result[1][3][2].getTag().name() == "EF"


def test_parse_sentence_list():
    result = tagger.tag("안녕하세요. 눈이 오는 설날 아침입니다.")
    result = parser.analyze(result)

    assert len(result) == 2
    assert len(result[0]) == 1
    assert len(result[1].getDependencies()) > 0


def test_parse_sentence():
    result = tagger.tagSentence("안녕하세요.")
    result = parser.analyze(result)
    assert type(result) is Sentence
    assert len(result.getDependencies()) > 0
    # assert result.root.dependents[0].target == 0
    assert result.surfaceString() == "안녕하세요 ."  # EUNJEON
    assert result[0].getSurface() == "안녕하세요"
    assert len(result[0]) == 4
    assert result[0][0].getSurface() == "안녕"