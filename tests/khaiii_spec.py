import os
import pytest

from koalanlp import *
from koalanlp.proc import *
from tests.proc_core_spec import test_Tagger_Sentence_typecheck


@pytest.fixture(scope="session")
def environ():
    Util.initialize(KHAIII="LATEST")
    tagger = Tagger(API.KHAIII, kha_resource=os.environ['KHAIII_RSC'])
    yield None, tagger, None, None, None
    del tagger
    Util.finalize()


def test_khaiii(environ):
    test_Tagger_Sentence_typecheck(environ)
