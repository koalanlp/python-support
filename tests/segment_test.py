from koalanlp import *
import pytest

initialize([API.TWITTER, API.EUNJEON], "1.9.2")
tagger = Tagger(API.EUNJEON)
segmenter = SentenceSplitter(API.TWITTER)

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
    result = tagger.tag_sentence("안녕하세요. 눈이 오는 설날 아침입니다.")
    result = sentences(result)
    assert len(result) == 2
    assert len(result[0]) == 2
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
