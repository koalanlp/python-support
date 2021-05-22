from typing import List, Tuple

from threading import Lock
from importlib import import_module
from kss import split_sentences

from koalanlp.data import Sentence, Word, Morpheme
from koalanlp.types import POS

try:
    _module = import_module('kiwipiepy')
    _KiwiClass = getattr(_module, 'Kiwi')
    _KiwiInstance = _KiwiClass()
    _KiwiInstance.prepare()
    _KiwiLock = Lock()
except Exception:
    raise ModuleNotFoundError('KoalaNLP는 Kiwi를 자동으로 설치하지 않습니다. 다음 명령으로 Kiwi를 설치해주세요:\n'
                              'pip install kiwipiepy')


def _convert_tag(raw_tag: str) -> str:
    raw_tag = raw_tag.upper()
    if raw_tag == 'UN':
        return 'NA'
    if raw_tag.startswith('W_'):
        return 'SW'
    return raw_tag


class Tagger:
    def tag(self, paragraph: str, no_split = False) -> List[Sentence]:
        # KSS를 사용해 문단을 문장들로 분리함
        if not no_split:
            sentences = split_sentences(paragraph)
        else:
            sentences = [paragraph]

        # Kiwi 실행
        _KiwiLock.acquire()
        kiwi_result = _KiwiInstance.analyze(sentences)
        _KiwiLock.release()

        # 변환
        result = []
        for sentence, analyzed in zip(sentences, kiwi_result):
            word_begin = 0
            word_end = 0
            words = []
            curr_morphs = []

            for morph, raw_tag, begin, length in analyzed[0][0]:
                if begin > word_end > word_begin:
                    # 공백문자가 사이에 있었으므로, 하나의 단어로 간주.
                    words.append(Word(sentence[word_begin:word_end], curr_morphs))
                    curr_morphs = []
                    word_begin = begin

                tag = _convert_tag(raw_tag)
                curr_morphs.append(Morpheme(morph, tag, raw_tag))
                word_end = begin + length

            # 모든게 종료되고 나서, 남은 형태소들 하나의 단어로 추가
            if curr_morphs:
                # 공백문자가 사이에 있었으므로, 하나의 단어로 간주.
                words.append(Word(sentence[word_begin:word_end], curr_morphs))

            # 문장 등록
            result.append(Sentence(words))

        return result

    def tagSentence(self, sentence: str) -> Sentence:
        return self.tag(sentence, no_split=True)[0]


class Dictionary:
    def addUserDictionary(self, *pairs: Tuple[str, POS]):
        """
        사용자 사전에, 표면형과 그 품사를 추가.

        :param Tuple[str,POS] pairs: (표면형, 품사)의 가변형 인자
        """
        _KiwiLock.acquire()
        for word, tag in pairs:
            _KiwiInstance.add_user_word(word, pos=tag.name)

        _KiwiInstance.prepare()
        _KiwiLock.release()

    def contains(self, word: str, *pos_tags: POS) -> bool:
        raise NotImplementedError()

    def importFrom(self, other, fastAppend=False, filter=lambda t: t.isNoun()):
        raise NotImplementedError()

    def getBaseEntries(self, filter=lambda t: t.isNoun()):
        raise NotImplementedError()

    def getItems(self) -> List[Tuple[str, POS]]:
        raise NotImplementedError()

    def getNotExists(self, onlySystemDic: bool, *word: Tuple[str, POS]) -> List[Tuple[str, POS]]:
        raise NotImplementedError()
