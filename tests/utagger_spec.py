import os
import pytest
from pathlib import Path

from koalanlp import *
from koalanlp.proc import *
from tests.proc_core_spec import compare_sentence, EXAMPLES


@pytest.fixture(scope="session")
def tagger():
    Util.initialize(UTAGGER="LATEST")

    travis_os = os.environ.get('TRAVIS_OS_NAME', 'linux')
    travis_dist = os.environ.get('TRAVIS_DIST', 'ubuntu')

    print(f'Recognized ${travis_os} ${travis_dist}.')

    utagger_path = Path(os.environ['HOME'], 'utagger').absolute()
    bin_path = os.path.join(utagger_path, 'bin')
    lib_path = "utagger-win64.dll" if travis_os == 'windows' else \
        ('utagger-ubuntu1804.so' if 'ubuntu' in travis_dist else 'utagger-centos7.so')

    lib_path = os.path.join(bin_path, lib_path)
    config_path = os.path.join(utagger_path, "Hlxcfg.txt")
    UTagger.setPath(lib_path, config_path)

    lines = Path(config_path).open(encoding='euc-kr').readlines()
    lines = [it.replace("HLX_DIR ../", "HLX_DIR %s/" % utagger_path) if it.startswith('HLX_DIR') else it
             for it in lines]
    Path(config_path).open('w+t', encoding='euc-kr').writelines(lines)
    tagger = Tagger(API.UTAGGER)
    yield tagger
    del tagger
    Util.finalize()


def test_utagger(tagger):
    for cnt, line in EXAMPLES:
        para = tagger(line)
        assert type(para) is list
        for sent in para:
            compare_sentence(sent, {'WSD': True})

        single = tagger.tagSentence(line)
        assert type(single) is list
        assert len(single) == 1

        compare_sentence(single[0], {'WSD': True})

        if cnt == 1 and len(para) == 1:
            assert len(para) == len(single)
        else:
            singles = tagger.tagSentence(*[sent.surfaceString() for sent in para])
            assert len(para) == len(singles)
