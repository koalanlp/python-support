# KoalaNLP (Python3 Support)

[![PyPI](https://img.shields.io/pypi/v/koalanlp.svg?style=flat-square)](https://github.com/koalanlp/python-support)
[![분석기별 품사비교표](https://img.shields.io/badge/%ED%92%88%EC%82%AC-%EB%B9%84%EA%B5%90%ED%91%9C-blue.svg?style=flat-square)](https://docs.google.com/spreadsheets/d/1OGM4JDdLk6URuegFKXg1huuKWynhg_EQnZYgTmG4h0s/edit?usp=sharing)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://tldrlegal.com/license/mit-license)
[![Sphinx doc](https://img.shields.io/badge/Python-Doc-blue.svg?style=flat-square)](https://koalanlp.github.io/python-support/html/)

[![Build Status](https://img.shields.io/travis/koalanlp/python-support.svg?style=flat-square&branch=master)](https://travis-ci.com/koalanlp/python-support)
[![codecov](https://codecov.io/gh/koalanlp/python-support/branch/master/graph/badge.svg)](https://codecov.io/gh/koalanlp/python-support)

[![java-koalanlp](https://img.shields.io/badge/Java,Kotlin-KoalaNLP-red.svg?style=flat-square)](https://koalanlp.github.io/koalanlp)
[![scala-koalanlp](https://img.shields.io/badge/Scala-KoalaNLP-blue.svg?style=flat-square)](https://koalanlp.github.io/scala-support)
[![nodejs-koalanlp](https://img.shields.io/badge/Nodejs-KoalaNLP-blue.svg?style=flat-square)](https://koalanlp.github.io/nodejs-support)

# 소개
한국어 형태소 및 구문 분석기의 모음인, [KoalaNLP](https://github.com/koalanlp/koalanlp)의 Python 판본입니다.

이 프로젝트는 __서로 다른 형태의 형태소 분석기를__ 모아,
__동일한 인터페이스__ 아래에서 사용할 수 있도록 하는 것이 목적입니다.

* 김상준님의 [Daon 분석기](https://github.com/rasoio/daon/tree/master/daon-core)

* Shineware의 [코모란 v3.3.9](https://github.com/shin285/KOMORAN)

* 서울대의 [꼬꼬마 형태소/구문 분석기 v2.1](http://kkma.snu.ac.kr/documents/index.jsp)

* ETRI의 [공공 인공지능 Open API](http://aiopen.etri.re.kr/)

* OpenKoreanText의 [오픈 소스 한국어 처리기 v2.3.1](http://openkoreantext.org) (구 Twitter 한국어 분석기)

* 은전한닢 프로젝트의 [SEunjeon(S은전) v1.5.0](https://bitbucket.org/eunjeon/seunjeon) (Mecab-ko의 Scala/Java 판본)

* 이수명님의 [Arirang Morpheme Analyzer](http://cafe.naver.com/korlucene) <sup>1-1</sup>

* 최석재님의 [RHINO v3.7.8](https://github.com/SukjaeChoi/RHINO)

* KAIST의 [한나눔 형태소 분석기](http://kldp.net/projects/hannanum/)와 [NLP_HUB 구문분석기](http://semanticweb.kaist.ac.kr/home/index.php/NLP_HUB)

* Kakao의 [카이(Khaiii) v0.4](https://github.com/kakao/khaiii) (별도설치 필요: [설치법](https://github.com/kakao/khaiii/wiki/빌드-및-설치))

* 울산대학교의 [UTagger 2018년 10월 31일자](http://nlplab.ulsan.ac.kr/doku.php?id=start) (별도설치 필요: [설치법](https://koalanlp.github.io/usage/Install-UTagger.md)) <sup>1-2</sup>

* 고현웅님의 [Korean Sentence Splitter v2.5.1](https://github.com/hyunwoongko/kss)

> <sup>주1-1</sup> Arirang 분석기의 출력을 형태소분석에 적합하게 조금 다듬었으므로, 원본과 약간 다른 결과를 낼 수도 있습니다.
>
> <sup>주1-2</sup> UTagger의 2019-7 버전도 공개되어 있지만, 리눅스 개발환경을 위한 라이브러리 파일이 공개되어있지 않아 지원하지 않습니다.

KoalaNLP의 Contributor가 되고 싶으시다면, 언제든지 Issue에 등록해주십시오.
또한, 추가하고자 하는 새로운 프로젝트가 있으시면, Issue에 등록해주십시오.

## 사용방법

* [Usage](https://koalanlp.github.io/koalanlp/usage/)
* [Sphinx Doc](http://koalanlp.github.io/python-support/html/)

## 특징

KoalaNLP는 다음과 같은 특징을 가지고 있습니다.

1. 복잡한 설정이 필요없는 텍스트 분석:

   모델은 자동으로 Maven으로 배포되기 때문에, 각 모델을 별도로 설치할 필요가 없습니다.

2. 코드 2~3 줄로 수행하는 텍스트 처리:

   모델마다 다른 복잡한 설정 과정, 초기화 과정은 필요하지 않습니다. Dependency에 추가하고, 객체를 생성하고, 분석 메소드를 호출하는 3줄이면 끝납니다.

3. 모델에 상관 없는 동일한 코드, 동일한 결과:

   모델마다 실행 방법, 실행 결과를 표현하는 형태가 다릅니다. KoalaNLP는 이를 정부 및 관계기관의 표준안에 따라 표준화합니다. 따라서 모델에 독립적으로 응용 프로그램 개발이 가능합니다.

4. Java, Kotlin, [Scala](https://koalanlp.github.io/scala-support), [Python 3](https://koalanlp.github.io/python-support), [NodeJS](https://koalanlp.github.io/nodejs-support)에서 크게 다르지 않은 코드:

   KoalaNLP는 여러 프로그래밍 언어에서 사용할 수 있습니다. 어디서 개발을 하더라도 크게 코드가 다르지 않습니다. 

# License 조항

이 프로젝트 자체(KoalaNLP-core)와 인터페이스 통합을 위한 코드는
소스코드에 저작권 귀속에 대한 별도 지시사항이 없는 한 v1.8.0부터 [*MIT License*](https://tldrlegal.com/license/mit-license)을 따르며,
원본 분석기의 License와 저작권은 각 저작권자가 지정한 바를 따릅니다.

단, GPL의 저작권 조항에 따라, GPL 하에서 이용이 허가되는 패키지들의 저작권은 해당 저작권 규정을 따릅니다.

* Hannanum 및 NLP_HUB: [GPL v3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3))

* KKMA: [GPL v2](https://tldrlegal.com/license/gnu-general-public-license-v2) (GPL v2를 따르지 않더라도, 상업적 이용시 별도 협의 가능)

* KOMORAN 3.x: [Apache License 2.0](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

* Open Korean Text: [Apache License 2.0](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

* SEunjeon: [Apache License 2.0](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

* 아리랑: [Apache License 2.0](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

* RHINO: [GPL v3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) (참고: 다운로드 위치별로 조항 상이함)

* Daon: 지정된 조항 없음

* ETRI: 별도 API 키 발급 동의 필요

* Khaiii: [Apache License 2.0](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

* UTagger: 교육 및 연구용으로 사용시 제한 없음. 상업용인 경우 울산대와 기술이전 등의 유료 협약 필요

* Korean Sentence Splitter(KSS): [BSD 3-Clause (Revised)](https://tldrlegal.com/license/bsd-3-clause-license-(revised))

# 사용법

## Dependency 추가
우선 Java JDK 8 이상을 설치하고, JDK의 설치 위치를 `JAVA_HOME`으로 하여 환경변수에 등록해주십시오.
그런 다음, 아래와 같이 설치하십시오. (현재 python-koalanlp 버전은 [![PyPI](https://img.shields.io/pypi/v/koalanlp.svg?style=flat-square)](https://github.com/koalanlp/python-support)입니다.)

* Python 3.7은 일부 의존 라이브러리의 문제로 인해 사용이 불가능합니다. 해당 라이브러리에서 문제를 해결하기 전까지는 3.6 이하를 사용해주세요.
* Windows나 OSX에서 미리 설치할 항목들은 [OS별 사전설치 항목](https://koalanlp.github.io/koalanlp/PlatformInstall.md)을 참고하세요.

```bash
$ pip install koalanlp
``` 

### Packages
각 형태소 분석기는 별도의 패키지로 나뉘어 있습니다.

| 패키지명            | 설명                                                                 |  사용 가능 버전    | License (원본)     |
| ------------------ | ------------------------------------------------------------------ | ---------------- | ----------------- |
| API.KMR          | 코모란 Wrapper, 분석범위: 형태소                                       | [![Ver-KMR](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-kmr.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-kmr%22)         | Apache 2.0 |
| API.EUNJEON      | 은전한닢 Wrapper, 분석범위: 형태소                                     | [![Ver-EJN](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-eunjeon.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-eunjeon%22) | Apache 2.0 |
| API.ARIRANG      | 아리랑 Wrapper, 분석범위: 형태소                                       | [![Ver-ARR](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-arirang.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-arirang%22) | Apache 2.0 |
| API.RHINO        | RHINO Wrapper, 분석범위: 형태소                                       | [![Ver-RHI](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-rhino.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-rhino%22)     | GPL v3 |
| API.DAON         | Daon Wrapper, 분석범위: 형태소                                        | [![Ver-DAN](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-daon.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-daon%22)       | MIT(별도 지정 없음) |
| API.KHAIII       | Khaiii Wrapper, 분석범위: 형태소 <sup>주2-3</sup>                                      | [![Ver-KHA](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-khaiii.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-khaiii%22)       | Apache 2.0 |
| API.UTAGGER      | 울산대 UTagger Wrapper / 분석범위: 형태소 <sup>2-4</sup>                                | [![Ver-UTA](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-utagger.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-utagger%22)       | 주2-4 |
| API.OKT          | Open Korean Text Wrapper, 분석범위: 문장분리, 형태소                    | [![Ver-OKT](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-okt.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-okt%22)        | Apache 2.0  |
| API.KKMA         | 꼬꼬마 Wrapper, 분석범위: 형태소, 의존구문                               | [![Ver-KKM](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-kkma.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-kkma%22)       | GPL v2    |
| API.HNN          | 한나눔 Wrapper, 분석범위: 문장분리, 형태소, 구문분석, 의존구문               | [![Ver-HNN](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-hnn.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-hnn%22)        | GPL v3    |
| API.ETRI         | ETRI Open API Wrapper, 분석범위: 형태소, 구문분석, 의존구문, 개체명, 의미역 | [![Ver-ETR](https://img.shields.io/maven-central/v/kr.bydelta/koalanlp-etri.svg?style=flat-square&label=r)](http://search.maven.org/#search%7Cga%7C1%7Ca%3A%22koalanlp-etri%22)      | MIT<sup>2-2</sup> |
| API.KSS          | Korean Sentence Splitter Wrapper, 분석범위: 문장분리                    | 버전무관 | BSD 3-Clause (Revised) |

> <sup>주2-2</sup> ETRI의 경우 Open API를 접근하기 위한 코드 부분은 KoalaNLP의 License 정책에 귀속되지만, Open API 접근 이후의 사용권에 관한 조항은 ETRI에서 별도로 정한 바를 따릅니다.
> 따라서, ETRI의 사용권 조항에 동의하시고 키를 발급하셔야 하며, 다음 위치에서 발급을 신청할 수 있습니다: [키 발급 신청](http://aiopen.etri.re.kr/key_main.php)
>
> <sup>주2-3</sup> Khaiii 분석기의 경우는 Java가 아닌 C++로 구현되어 사용 전 분석기의 설치가 필요합니다. Python3.6 및 CMake 3.10+만 설치되어 있다면 설치 자체가 복잡한 편은 아니니 [여기](https://github.com/kakao/khaiii/blob/v0.1/doc/setup.md)를 참조하여 설치해보세요. (단, v0.1에서는 빌드시 'python3' 호출시 'python3.6'이 연결되어야 합니다.) 참고로, KoalaNLP가 Travis CI에서 패키지를 자동 테스트하기 위해 구현된 bash script는 [여기](https://github.com/koalanlp/koalanlp/blob/master/khaiii/install.sh)에 있습니다.
>
> <sup>주2-4</sup> UTagger 분석기의 경우에도 C/C++로 구현되어, 사용 전 분석기의 설치가 필요합니다. 윈도우와 리눅스(우분투, CentOS)용 라이브러리 파일만 제공되며, 설치 방법은 [여기](https://koalanlp.github.io/usage/Install-UTagger.md)를 참조하십시오. UTagger 분석기는 교육 연구용은 무료로 배포되며, 상업용은 별도 협약이 필요합니다.

### 초기화
초기화 과정에서 KoalaNLP는 필요한 Java Library를 자동으로 다운로드하여 설치합니다. 설치에는 시간이 다소 소요됩니다.
때문에, 프로그램 실행시 최초 1회에 한하여 초기화 작업이 필요합니다.

> *참고*: KSS만 사용하는 경우, 초기화 과정이 필요하지 않습니다.

```python
from koalanlp.Util import initialize, finalize

# 꼬꼬마와 은전한닢 분석기의 2.0.0 버전을 참조합니다.
initialize(java_options="-Xmx4g", KKMA="2.0.2", ETRI="2.0.2")
# 사용이 끝나면 반드시 finalize를 호출합니다.
finalize()
```

* `java_options` 인자는 JVM을 실행하기 위한 option string입니다.
* 이후 인자들은 keyword argument들로, 상단 표를 참고하여 지정하실 수 있습니다.
* 키워드가 지정되지 않으면 다음 코드와 같은 효과를 나타냅니다: `KMR="LATEST"`
* 나머지 문서는 초기화 과정이 모두 완료되었다고 보고 진행합니다.
* API 참고: [initialize](https://koalanlp.github.io/python-support/html/koalanlp.html#koalanlp.Util.initialize)

## 간단한 예시
다음과 같이 사용합니다.
```python
from koalanlp.Util import initialize, finalize
from koalanlp.proc import *
from koalanlp import API

# 초기화 합니다.
initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2", EUNJEON="2.0.2", ETRI="2.0.2")

# 품사분석기 이용법
tagger = Tagger(API.EUNJEON)
tagged = tagger.tag("안녕하세요. 눈이 오는 설날 아침입니다.")
print(tagged)

# 의존구문분석기 이용법
parser = Parser(API.KKMA)
parsed = parser.analyze("안녕하세요. 눈이 오는 설날 아침입니다.")
print(parsed)

# ETRI API 이용법
ETRI_API_KEY = "......"  # ETRI에서 발급받은 키를 입력하세요.
rolelabeler = RoleLabeler(API.ETRI, ETRI_API_KEY)
paragraph = rolelabeler.analyze("첫 분석을 시도해봅시다!")
print(paragraph)
print(paragraph[0].getRoles())

# Data classes
sentence = parsed[1] # 두번째 문장인, "눈이 오는 설날 아침입니다."를 선택합니다.

wordAt0 = sentence[0] # 첫번째 어절을 선택해봅니다.
print(wordAt0.exists(lambda m: m.isPredicate())) # 첫번째 어절에, 용언(동사/형용사)을 포함한 형태소가 있는지 확인합니다.
print(sentence.exists(lambda w: w.exists(lambda m: m.isNoun()))) # 문장 전체에 체언(명사 등)을 포함한 어절이 있는지 확인합니다.
print(sentence.getNouns()) # 문장에서 체언만 추출합니다.
print(sentence.getVerbs()) # 문장에서 용언만 추출합니다.

finalize() # KoalaNLP 사용을 종료합니다.
```

# 결과 비교
[Sample:결과비교](https://koalanlp.github.io/sample/comparison)를 참조해주세요.
