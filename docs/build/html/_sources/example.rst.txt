간단한 예시
============

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
