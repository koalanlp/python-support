from koalanlp import *
from koalanlp.jvm import is_jvm_running
from koalanlp.proc import *
import pytest
import inspect
import multiprocessing


def init_and_finalize(port):
    Util.initialize(EUNJEON="LATEST", port=port)
    if not is_jvm_running():
        return -1

    tagger = Tagger(api=API.EUNJEON)
    tagger("하나의 예시 문장입니다.")

    del tagger
    if not Util.finalize():
        return -1
    if is_jvm_running():
        return -1

    return 1


def test_init_finalize_tagger():
    pool = multiprocessing.Pool(4)

    results = pool.imap_unordered(init_and_finalize, [51111, 51112, 51113, 51114, 51115, 51116])
    assert all(res > 0 for res in results)
