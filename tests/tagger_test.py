from koalanlp import *
import pytest

initialize([API.EUNJEON], "1.9.2")
tagger = Tagger(API.EUNJEON)

def test_tag_sentence():
    result = tagger.tag_sentence("안녕하세요.")
    assert not type(result) is list
    assert type(result) is Sentence
    assert len(result) == 2
    assert result.surface_string() == "안녕하세요 ."
    assert result[0].surface == "안녕하세요"
    assert len(result[0]) == 4
    assert result[0][0].surface == "안녕"

    result = tagger.tag_sentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert not type(result) is list
    assert len(result) == 7

def test_tag():
    result = tagger.tag("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert type(result) is list
    assert len(result) == 2
    assert len(result[0]) == 2
    assert type(result[0]) is Sentence
    assert result[0].surface_string() == "안녕하세요 ."
    assert result[0][0].surface == "안녕하세요"
    assert len(result[1]) == 5
    assert result[1].surface_string() == "눈이 오는 설날 아침입니다 ."
    assert result[1][0].surface == "눈이"
    assert result[1][0][0].surface == "눈"
    assert result[1][0][0].tag == "NNG"
    assert result[1][0][0].raw_tag == "NNG"
    assert result[1][0][1].surface == "이"
    assert result[1][0][1].raw_tag == "JKS"
    assert result[1][3].surface == "아침입니다"
    assert result[1][3][2].surface == "ᄇ니다"
    assert result[1][3][2].tag == "EF"
