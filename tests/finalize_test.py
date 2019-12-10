from koalanlp import *
from koalanlp.jvm import is_jvm_running
from koalanlp.proc import *
import pytest
import inspect


def test_init_finalize_tagger():
    Util.initialize(EUNJEON="LATEST")
    assert is_jvm_running()
    tagger = Tagger(api=API.EUNJEON)

    # Reference will be changed
    tagged_before = ''.join([str(sent) for sent in tagger("하나의 예시 문장입니다.")])

    del tagger
    assert Util.finalize()
    assert not is_jvm_running()

    # clear all and initialize
    Util.initialize(EUNJEON="LATEST", force_download=True)
    assert is_jvm_running()

    tagger = Tagger(api=API.EUNJEON)
    tagged_after = ''.join([str(sent) for sent in tagger("하나의 예시 문장입니다.")])

    del tagger
    assert tagged_before == tagged_after
    assert Util.finalize()
