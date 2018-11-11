.. KoalaNLP documentation master file, created by
   sphinx-quickstart on Sat Jan  6 00:50:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


========
KoalaNLP
========

소개
=====

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


문서
====

.. toctree::
    주요 기능 사용법 <https://koalanlp.github.io/koalanlp/usage/>
    koalanlp
    Kotlin/Java API <https://koalanlp.github.io/koalanlp/api/koalanlp/index.html>
    Scala API <https://koalanlp.github.io/scala-support>
    NodeJS API <https://koalanlp.github.io/nodejs-support>

색인
====

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

