.. KoalaNLP documentation master file, created by
   sphinx-quickstart on Sat Jan  6 00:50:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


===========
KoalaNLP
===========

소개
====
한국어 형태소 및 구문 분석기의 모음인,
`KoalaNLP <https://github.com/nearbydelta/koalanlp>`__\ 의 Python
판본입니다.

이 프로젝트는 **서로 다른 형태의 형태소 분석기를** 모아, **동일한
인터페이스** 아래에서 사용할 수 있도록 하는 것이 목적입니다.

-  Hannanum: KAIST의 `한나눔 형태소
   분석기 <http://kldp.net/projects/hannanum/>`__\ 와 `NLP\_HUB
   구문분석기 <http://semanticweb.kaist.ac.kr/home/index.php/NLP_HUB>`__

-  KKMA: 서울대의 `꼬꼬마 형태소/구문
   분석기 <http://kkma.snu.ac.kr/documents/index.jsp>`__

-  KOMORAN: Junsoo
   Shin님의 `코모란 v3.x <https://github.com/shin285/KOMORAN>`__

-  Twitter: OpenKoreanText의 `오픈 소스 한국어
   처리기 <http://openkoreantext.org>`__ (구 Twitter 한국어 분석기) 1-1

-  Eunjeon: 은전한닢 프로젝트의
   `SEunjeon(S은전) <https://bitbucket.org/eunjeon/seunjeon>`__
-  Arirang:
   이수명님의 `Arirang Morpheme
   Analyzer <http://cafe.naver.com/korlucene>`__ 1-2

-  RHINO: 최석재님의
   `RHINO v2.5.4 <https://github.com/SukjaeChoi/RHINO>`__

    주1-1 이전 코드와의 연속성을 위해서, OpenKoreanText의 패키지 명칭은
    twitter로 유지합니다.

    주1-2 Arirang 분석기의 출력을 형태소분석에 적합하게 조금
    다듬었으므로, 원본과 약간 다른 결과를 낼 수도 있습니다.

KoalaNLP의 Contributor가 되고 싶으시다면, 언제든지 Issue에
등록해주십시오. 또한, 추가하고자 하는 새로운 프로젝트가 있으시면,
Issue에 등록해주십시오.



사용법
======
Dependency 추가
---------------

-  ``Java`` 8 이상이 설치되어 있고, ``JAVA_HOME``\ 이 설정되어 있어야
   합니다.
-  Python 3.5 이상 지원합니다.

아래와 같이 ``koalanlp``\ 를 추가해주세요.

.. code:: shell

    $ pip install Cython
    $ pip install koalanlp

만약, 설치에 문제가 생기면, ``Cython``, ``pyjnius``, ``jip``\ 를 먼저
설치해주세요.

간단한 예시
-----------

``koalanlp``\ 는, ``pyjnius`` 및 ``jip`` 패키지의 도움을 받아, 필요한
java dependency를 자동으로 가져옵니다.

    [참고] 최초 사용시 또는, 최신 패키지로 업데이트 되는 경우,
    dependency를 찾아오는 데 시간이 소요될 수 있습니다.

다음과 같이 사용합니다.

.. code:: python

    from koalanlp.api import *
    from koalanlp.data import POS

    # 초기화 합니다.
    initialize(packages=[API.KKMA, API.EUNJEON], version="1.9.1", java_options="-Xmx4g")

    # 품사분석기 이용법
    tagger = Tagger(tagger_type=API.EUNJEON)

    # POS Tagging
    tagged = tagger.tag("안녕하세요. 눈이 오는 설날 아침입니다.")
    print(str(tagged))

    # 의존구문분석기 이용법
    parser = Parser(tagger_type=API.EUNJEON, parser_type=API.KKMA)

    # Dependency Parsing
    parsed = parser.parse("안녕하세요. 눈이 오는 설날 아침입니다.")
    print(str(parsed))

    # Data classes
    sentence = parsed[1] # 두번째 문장인, "눈이 오는 설날 아침입니다."를 선택합니다.

    wordAt0 = sentence[0] # 첫번째 어절을 선택해봅니다.
    print(wordAt0.exists(lambda m: POS.is_predicate(m.tag))) # 첫번째 어절에, 용언(동사/형용사)을 포함한 형태소가 있는지 확인합니다.
    print(sentence.exists(lambda w: w.exists(lambda m: POS.is_noun(m.tag)))) # 문장 전체에 체언(명사 등)을 포함한 어절이 있는지 확인합니다.
    print(sentence.nouns()) # 문장에서 체언만 추출합니다.
    print(sentence.verbs()) # 문장에서 용언만 추출합니다.

사용가능한 패키지 목록
----------------------

+----------------+---------------------------+----------------------+-------------------------+--------------------------+---------------------------+-------------------------+-----------------------+
|                | 은전한닢(\ ``EUNJEON``)   | 꼬꼬마(\ ``KKMA``)   | 코모란(\ ``KOMORAN``)   | 한나눔(\ ``HANNANUM``)   | 오픈한글(\ ``TWITTER``)   | 아리랑(\ ``ARIRANG``)   | 라이노(\ ``RHINO``)   |
+================+===========================+======================+=========================+==========================+===========================+=========================+=======================+
| 품사분석       | v1.4.0                    | v2                   | v3.3.3                  | v1                       | v2.1.2                    | v1.1.3                  | v2.5.4                |
+----------------+---------------------------+----------------------+-------------------------+--------------------------+---------------------------+-------------------------+-----------------------+
| 의존구문분석   | 지원안함                  | 가능                 | 지원안함                | 가능                     | 지원안함                  | 지원안함                | 지원안함              |
+----------------+---------------------------+----------------------+-------------------------+--------------------------+---------------------------+-------------------------+-----------------------+



API
===
.. toctree::
    modules



색인
====
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

