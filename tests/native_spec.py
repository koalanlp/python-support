import pytest

from koalanlp import *
from koalanlp.proc import *
from tests.proc_core_spec import EXAMPLES

from kss import split_sentences
from kiwipiepy import Kiwi


@pytest.fixture(scope="session")
def environ():
    Util.initialize(KSS="LATEST")
    ssplit = SentenceSplitter(API.KSS)
    tagger = Tagger(API.KIWI)
    yield ssplit, tagger
    del ssplit
    del tagger
    Util.finalize()


def test_kss_empty(environ):
    splitter, _ = environ
    sentences = splitter.sentences("")
    assert len(sentences) == 0


def test_kss_equal(environ):
    splitter, _ = environ
    for _, line in EXAMPLES:
        res1 = splitter(line)
        res2 = split_sentences(line)
        assert res1 == res2


def test_kiwi_empty(environ):
    _, tagger = environ
    sentences = tagger.tag("")
    assert len(sentences) == 0


def test_kiwi(environ):
    _, tagger = environ
    kiwi = Kiwi()
    kiwi.prepare()

    for _, line in EXAMPLES:
        res1 = tagger.tagSentence(line)[0]
        res2 = kiwi.analyze(line)

        res1 = [(m.surface, m.originalTag) for w in res1 for m in w]
        res2 = [m[:2] for m in res2[0][0]]

        assert res1 == res2
