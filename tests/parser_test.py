from koalanlp import *
import pytest

initialize([API.EUNJEON, API.KKMA], "1.9.2")
parser1 = Parser(API.KKMA)
parser2 = Parser(API.KKMA, API.EUNJEON)
tagger = Tagger(API.EUNJEON)

def test_parse_sentence():
    with pytest.raises(Exception):
        parser1.parse_sentence("안녕하세요.")

    with pytest.raises(Exception):
        parser1.parse_sentence("안녕하세요. 눈이 오는 설날 아침입니다.")

def test_parse():
    result = parser1.parse("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert len(result) == 2
    assert len(result[0]) == 1
    assert type(result[0]) is Sentence
    assert result[0].surface_string() == "안녕하세요." #KKMA
    assert result[0][0].surface == "안녕하세요."
    assert len(result[1]) == 4
    assert len(result[1].root.dependents) > 0
    assert result[1].root.dependents[0].target == 3
    assert result[1].surface_string() == "눈이 오는 설날 아침입니다." #KKMA
    assert result[1][0].surface == "눈이"
    assert result[1][0][0].surface == "눈"
    assert result[1][0][0].tag == "NNG"
    assert result[1][0][0].raw_tag == "NNG"
    assert result[1][0][1].surface == "이"
    assert result[1][0][1].raw_tag == "JKS"
    assert result[1][3].surface == "아침입니다."
    assert result[1][3][2].surface == "ㅂ니다" #KKMA (받침아님)
    assert result[1][3][2].tag == "EF"

def test_parse_sentence_relay():
    result = parser2.parse_sentence("안녕하세요.")
    assert not type(result) is list
    assert type(result) is Sentence
    assert len(result) == 2
    assert len(result.root.dependents) > 0
    assert result.root.dependents[0].target == 0
    assert result.surface_string() == "안녕하세요 ." #EUNJEON
    assert result[0].surface == "안녕하세요"
    assert len(result[0]) == 4
    assert result[0][0].surface == "안녕"

    result = parser2.parse_sentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    assert not type(result) is list
    assert len(result) == 7
    assert len(result.root.dependents) > 0
    assert result.root.dependents[0].target == 1

    result2 = tagger.tag_sentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    result2 = parser1.parse_sentence(result2)

    zipped = zip(iter(result), iter(result2))
    for (a, b) in zipped:
        assert a == b
