from typing import List
from importlib import import_module


class SentenceSplitter:
    def __init__(self):
        try:
            module = import_module('kss')
            self._call = getattr(module, 'split_sentences')
        except ModuleNotFoundError:
            raise Exception('KSS Python package를 설치해야 합니다. 다음 명령을 실행하세요:\n pip install kss')

    def invoke(self, paragraph) -> List[str]:
        if paragraph:
            return self._call(paragraph)
        else:
            return []
