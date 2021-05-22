import os
import pytest

from koalanlp import *
from koalanlp.proc import *
from tests.proc_core_spec import test_Tagger_Sentence_typecheck as typecheck


@pytest.fixture(scope="session")
def environ():
    lib_path = os.environ['KHAIII_LIB']
    Util.initialize(KHAIII="LATEST", java_options="-Xmx1g -Dfile.encoding=utf-8 -Djna.library.path=%s" % lib_path)
    tagger = Tagger(API.KHAIII, kha_resource=os.environ['KHAIII_RSC'])
    yield None, tagger, None, None, None
    del tagger
    Util.finalize()


def test_khaiii(environ):
    typecheck(environ)
