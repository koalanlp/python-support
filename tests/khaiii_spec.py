import os
import pytest

from koalanlp import *
from koalanlp.proc import *
from tests.proc_core_spec import test_Tagger_Sentence_typecheck


@pytest.fixture(scope="session")
def environ():
    lib_path = os.environ['KHAIII_LIB']
    os.environ['LD_LIBRARY_PATH'] = '%s:%s' % (lib_path, os.environ.get('LD_LIBRARY_PATH', ''))

    Util.initialize(KHAIII="LATEST")
    tagger = Tagger(API.KHAIII, kha_resource=os.environ['KHAIII_RSC'])
    yield None, tagger, None, None, None
    del tagger
    Util.finalize()


def test_khaiii(environ):
    test_Tagger_Sentence_typecheck(environ)
