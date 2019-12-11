from koalanlp import *
from koalanlp.proc import *
from koalanlp.data import *
from koalanlp.types import *
from koalanlp.jvm import *
import os
import random
import pytest
from time import sleep


@pytest.fixture(scope="session")
def environ():
    Util.initialize(OKT="LATEST", HNN="LATEST", ETRI="LATEST")
    splitter = SentenceSplitter(API.OKT)
    tagger = Tagger(API.OKT)
    parser = Parser(API.HNN)
    entityRecog = EntityRecognizer(API.ETRI, etri_key=os.environ['API_KEY'])
    roleLabeler = RoleLabeler(API.ETRI, etri_key=os.environ['API_KEY'])

    yield splitter, tagger, parser, entityRecog, roleLabeler
    Util.finalize()


# Reduced set of examples for python test
EXAMPLES = [line.strip().split(' ', maxsplit=1)
            for text in [
                """01 1+1은 2이고, 3*3은 9이다.
                01 RHINO는 말줄임표를... 확인해야함... ^^ 이것도 확인해야.
                03 식사함은 식사에서부터인지 식사에서부터이었는지 살펴봄. 보기에는 살펴봄이 아리랑을 위한 시험임을 지나쳤음에. 사랑하였음은 사랑해봄은 보고싶기에 써보기에 써보았기에.
                03 먹음이니. 먹음이었으니. 사면되어보았기에.
                01 a/b는 분수이다.
                01 | 기호는 분리기호이다.
                02 ▶ 오늘의 날씨입니다. ◆ 기온 23도는 낮부터임.
                01 【그】가 졸음이다. 사랑스러웠기에.
                01 [Dr.브레인 - 마루투자자문 조인갑 대표]
                01 [결 마감특징주 - 유진투자증권 갤러리아지점 나현진 대리]
                01 진경복 한기대 산학협력단장은 "이번 협약 체결로 우수한 현장 기능 인력에 대한 대기업-중소기업간 수급 불균형 문제와 중소·중견기업들에 대한 취업 기피 현상을 해결할 것"이라며 "특성화 및 마이스터고 학생들을 대학에 진학시켜 자기계발 기회를 제공하는 국내 최초의 상생협력 모델이라는 점에 의미가 있다"고 강조했다.
                01 [결 마감특징주 - 신한금융투자 명품PB강남센터 남경표 대리]
                01 [Dr.브레인 - 마루투자자문 조인갑 대표]
                01 '플라이 아웃'은 타자가 친 공이 땅에 닿기 전에 상대팀 야수(투수와 포수를 제외한 야수들-1·2·3루수, 좌익수, 중견수, 우익수, 유격수)가 잡는 것, '삼진 아웃'은 스트라이크가 세 개가 되어 아웃되는 것을 말한다.
                01 대선 출마를 선언한 민주통합당 손학규 상임고문이 5일 오후 서울 세종문화회관 세종홀에서 열린 '저녁이 있는 삶-손학규의 민생경제론'출판기념회에서 행사장으로 들어서며 손을 들어 인사하고 있다.2012.7.5/뉴스1""".strip(),

                # Example 1: JTBC, 2017.04.22
                """03 북한이 도발을 멈추지 않으면 미국이 북핵 시설을 타격해도 군사개입을 하지 않겠다. 중국 관영 환구시보가 밝힌 내용인데요. 중국이 여태껏 제시한 북한에 대한 압박 수단 가운데 가장 이례적이고, 수위가 높은 것으로 보입니다.
                01 이한주 기자입니다.
                02 중국 관영매체 환구시보가 북핵문제에 대해 제시한 중국의 마지노선입니다. 북핵 억제를 위해 외교적 노력이 우선해야 하지만 북한이 도발을 지속하면 핵시설 타격은 용인할 수 있다는 뜻을 내비친 겁니다.
                02 그러나 한국과 미국이 38선을 넘어 북한 정권 전복에 나서면 중국이 즉각 군사개입에 나서야 한다는 점을 분명히 하였습니다. 북한에 대한 압박수위도 한층 높였습니다.
                02 핵실험을 강행하면 트럼프 대통령이 북한의 생명줄로 지칭한 중국의 원유공급을 대폭 축소할 거라고 경고하였습니다. 축소 규모에 대해서도 '인도주의적 재앙이 일어나지 않는 수준'이라는 기준까지 제시하며 안보리 결정을 따르겠다고 못 박았습니다.
                02 중국 관영매체가 그동안 북한에 자제를 요구한 적은 있지만, 군사지원 의무제공 포기 가능성과 함께 유엔 안보리 제재안을 먼저 제시한 것은 이례적입니다. 미·중 빅딜에 따른 대북압박 공조 가능성이 제기되는 가운데 북한이 어떤 반응을 보일지 관심이 쏠립니다.""".strip(),

                # Example 3. 허핑턴포스트, 17.04.22
                """01 박근혜 전 대통령이 거주하던 서울 삼성동 자택은 홍성열 마리오아울렛 회장(63)이 67억5000만원에 매입한 것으로 확인되었다.
                01 홍 회장은 21일 뉴스1과의 통화에서 "값이 싸게 나오고 위치가 좋아서 삼성동 자택을 사게 되었다"고 밝혔다.
                01 홍 회장은 "제가 강남에 집이나 땅이 하나도 없어서 알아보던 중에 부동산에 아는 사람을 통해서 삼성동 자택이 매물로 나온 걸 알게 되었다"며 "처음에는 조금 부담되었지만 집사람도 크게 문제가 없다고 해서 매입하였다"고 말하였다.
                01 이어 "조만간 이사를 할 생각이지만 난방이나 이런게 다 망가졌다기에 보고나서 이사를 하려한다"며 "집부터 먼저 봐야될 것 같다"고 하였다.
                01 홍 회장은 한때 자택 앞에서 박 전 대통령 지지자들의 집회로 주민들이 큰 불편을 겪었던 것과 관련 "주인이 바뀌면 그런 일을 할 이유가 없을 것이라 생각한다"고 밝혔다.
                01 박 전 대통령과의 인연 등에 대해선 "정치에 전혀 관심이 없고 그런(인연) 건 전혀 없다"며 "박 전 대통령 측이나 친박계 의원 측과의 접촉도 전혀 없었다"고 전하였다.
                01 홍 회장은 일부 언론보도로 알려진 박지만 EG회장과의 친분설도 "사실과 다르다"며 "박 전 대통령 사돈의 팔촌과도 인연이 없다"고 거듭 강조하였다.
                02 홍 회장에 따르면 자택 매입가는 67억5000만원이다. 홍 회장은 주택을 매입하면서 2억3600만원의 취득세를 납부하였다고 밝혔다.
                01 홍 회장은 1980년 마리오상사를 설립한 뒤 2001년 마리오아울렛을 오픈하며 의류 판매업 등으로 국내 최대급 아울렛으로 성장시켰다.
                01 한편 박 전 대통령은 최근 삼성동 자택을 매각하고 내곡동에 새 집을 장만한 것으로 확인되었으며 이달 중 내곡동으로 이삿짐을 옮길 것으로 알려졌다.""".strip()]
            for line in text.split('\n')]
EXAMPLES = [(int(t[0]), t[1]) for t in EXAMPLES]


def compare_morphemes(pymorph, opts):
    assert type(pymorph) is Morpheme
    assert pymorph.getId() == pymorph.reference.getId()
    assert pymorph.getTag().name == pymorph.reference.getTag().name()
    assert pymorph.getOriginalTag() == pymorph.reference.getOriginalTag()
    assert pymorph.getSurface() == pymorph.reference.getSurface()
    assert pymorph.getWord().reference.equals(pymorph.reference.getWord())
    assert pymorph.reference.equals(pymorph.getReference())

    if opts.get('NER', False) and pymorph.reference.getEntities() is not None:
        pyents = [e.reference for e in pymorph.getEntities()]
        jents = pymorph.reference.getEntities()
        assert all(jents.contains(e) for e in pyents)
    else:
        assert len(pymorph.getEntities()) == 0

    if opts.get('WSD', False):
        assert pymorph.getWordSense() == pymorph.reference.getWordSense()
    else:
        assert pymorph.getWordSense() is None

    assert pymorph.isJosa() == pymorph.reference.isJosa()
    assert pymorph.isModifier() == pymorph.reference.isModifier()
    assert pymorph.isNoun() == pymorph.reference.isNoun()
    assert pymorph.isPredicate() == pymorph.reference.isPredicate()

    assert all(pymorph.hasTag(tag.name) == pymorph.reference.hasTag(string(tag.name)) for tag in POS.values())

    sampled = random.sample([x.name for x in POS.values()], 3)
    assert pymorph.hasTagOneOf(*sampled) == pymorph.reference.hasTagOneOf(java_varargs([string(x) for x in sampled],
                                                                                       class_of('java.lang.String')))

    assert str(pymorph) == pymorph.reference.toString()


def compare_words(pyword, opts):
    assert type(pyword) is Word

    for morph in pyword:
        assert pyword.reference.contains(morph.reference)
        compare_morphemes(morph, opts)

    assert pyword.getSurface() == pyword.reference.getSurface()
    assert pyword.getId() == pyword.reference.getId()
    assert pyword.singleLineString() == pyword.reference.singleLineString()
    assert pyword.reference.equals(pyword.getReference())

    if opts.get('NER', False) and pyword.reference.getEntities() is not None:
        pyents = [e.reference for e in pyword.getEntities()]
        jents = pyword.reference.getEntities()
        assert all(jents.contains(e) for e in pyents)
    else:
        assert len(pyword.getEntities()) == 0

    if opts.get('SRL', False):
        if pyword.reference.getPredicateRoles() is not None:
            pyargs = [e.reference for e in pyword.getPredicateRoles()]
            jargs = pyword.reference.getPredicateRoles()
            assert all(jargs.contains(e) for e in pyargs)

        if pyword.reference.getArgumentRoles() is not None:
            pyargs = [e.reference for e in pyword.getArgumentRoles()]
            jargs = pyword.reference.getArgumentRoles()
            assert all(jargs.contains(e) for e in pyargs)
    else:
        assert len(pyword.getPredicateRoles()) == 0
        assert len(pyword.getArgumentRoles()) == 0

    if opts.get('DEP', False):
        if pyword.reference.getGovernorEdge() is not None:
            assert pyword.getGovernorEdge().reference.equals(pyword.reference.getGovernorEdge())

        if pyword.reference.getDependentEdges() is not None:
            pyargs = [e.reference for e in pyword.getDependentEdges()]
            jargs = pyword.reference.getDependentEdges()
            assert all(jargs.contains(e) for e in pyargs)
    else:
        assert pyword.getGovernorEdge() is None
        assert len(pyword.getDependentEdges()) == 0

    if opts.get('SYN', False):
        assert pyword.getPhrase().reference.equals(pyword.reference.getPhrase())
    else:
        assert pyword.getPhrase() is None

    assert str(pyword) == pyword.reference.toString()


def compare_phrase(pytree):
    assert type(pytree) is SyntaxTree
    assert pytree.getLabel().name == pytree.reference.getLabel().name()
    assert pytree.hasNonTerminals() == pytree.reference.hasNonTerminals()
    assert pytree.isRoot() == pytree.reference.isRoot()
    assert pytree.getOriginalLabel() == pytree.reference.getOriginalLabel()
    assert pytree.getTreeString() == pytree.reference.getTreeString().toString()
    assert pytree.reference.equals(pytree.getReference())

    pyterms = [t.reference for t in pytree.getTerminals()]
    jterms = pytree.reference.getTerminals()
    assert all(jterms.contains(t) for t in pyterms)

    pynterms = [t.reference for t in pytree.getNonTerminals()]
    jnterms = pytree.reference.getNonTerminals()
    assert all(jnterms.contains(t) for t in pynterms)

    if not pytree.reference.isRoot():
        assert pytree.getParent().reference.equals(pytree.reference.getParent())
    else:
        assert pytree.getParent() is None

    jterm = pytree.reference.getTerminal()
    if jterm is not None:
        assert pytree.getTerminal().reference.equals(jterm)
    else:
        assert pytree.getTerminal() is None

    for nonterm in pytree:
        assert pytree.reference.contains(nonterm.reference)
        compare_phrase(nonterm)

    assert str(pytree) == pytree.reference.toString()


def compare_depedge(pyedge):
    assert type(pyedge) is DepEdge
    assert pyedge.getOriginalLabel() == pyedge.reference.getOriginalLabel()
    assert pyedge.getType().name == pyedge.reference.getType().name()
    assert pyedge.reference.equals(pyedge.getReference())

    gov = pyedge.getGovernor()
    if pyedge.reference.getGovernor() is not None:
        assert gov.reference.equals(pyedge.reference.getGovernor())
        assert pyedge.getSrc().reference.equals(pyedge.reference.getSrc())
        assert gov == pyedge.getSrc()
    else:
        assert pyedge.reference.getGovernor() is None
        assert pyedge.reference.getSrc() is None
        assert gov is None
        assert pyedge.getSrc() is None

    assert pyedge.getDependent().reference.equals(pyedge.reference.getDependent())
    assert pyedge.getDest().reference.equals(pyedge.reference.getDest())
    assert pyedge.getDependent() == pyedge.getDest()

    deptyp = pyedge.getDepType()
    if pyedge.reference.getDepType() is not None:
        assert deptyp.name == pyedge.reference.getDepType().name()
        assert pyedge.getLabel().name == pyedge.reference.getLabel().name()
        assert pyedge.getDepType() == pyedge.getLabel()
    else:
        assert pyedge.getLabel() is None
        assert pyedge.getDepType() is None

    assert str(pyedge) == pyedge.reference.toString()


def compare_roleedge(pyedge):
    assert type(pyedge) is RoleEdge
    assert pyedge.getOriginalLabel() == pyedge.reference.getOriginalLabel()
    assert pyedge.getLabel().name == pyedge.reference.getLabel().name()
    assert pyedge.reference.equals(pyedge.getReference())

    gov = pyedge.getPredicate()
    if pyedge.reference.getPredicate() is not None:
        assert gov.reference.equals(pyedge.reference.getPredicate())
        assert pyedge.getSrc().reference.equals(pyedge.reference.getSrc())
        assert gov == pyedge.getSrc()
    else:
        assert pyedge.reference.getPredicate() is None
        assert pyedge.reference.getSrc() is None
        assert gov is None
        assert pyedge.getSrc() is None

    assert pyedge.getArgument().reference.equals(pyedge.reference.getArgument())
    assert pyedge.getDest().reference.equals(pyedge.reference.getDest())
    assert pyedge.getArgument() == pyedge.getDest()

    assert str(pyedge) == pyedge.reference.toString()


def compare_entity(pyentity):
    assert type(pyentity) is Entity
    assert pyentity.getLabel().name == pyentity.reference.getLabel().name()
    assert pyentity.getOriginalLabel() == pyentity.reference.getOriginalLabel()
    assert pyentity.getSurface() == pyentity.reference.getSurface()
    assert pyentity.getFineLabel() == pyentity.reference.getFineLabel()
    assert pyentity.reference.equals(pyentity.getReference())
    # assert pyentity.getCorefGroup().reference.equals(pyentity.reference.getCorefGroup())

    for id, morph in enumerate(pyentity):
        assert type(morph) is Morpheme
        assert pyentity.reference.contains(morph.reference)
        assert pyentity.reference.get(id).equals(morph.reference)

    assert str(pyentity) == pyentity.reference.toString()


def compare_sentence(pysent, opts={}):
    assert type(pysent) is Sentence
    assert str(pysent) == pysent.reference.toString()
    assert pysent.singleLineString() == pysent.reference.singleLineString()
    assert pysent.reference.equals(pysent.getReference())

    assert pysent.surfaceString() == pysent.reference.surfaceString()
    assert pysent.surfaceString('//') == pysent.reference.surfaceString(string('//'))

    if opts.get('NER', False):
        for ent in pysent.getEntities():
            assert pysent.reference.getEntities().contains(ent.reference)
            compare_entity(ent)
    else:
        assert len(pysent.getEntities()) == 0

    if opts.get('DEP', False):
        for dep in pysent.getDependencies():
            assert pysent.reference.getDependencies().contains(dep.reference)
            compare_depedge(dep)
    else:
        assert len(pysent.getDependencies()) == 0

    if opts.get('SRL', False):
        for role in pysent.getRoles():
            assert pysent.reference.getRoles().contains(role.reference)
            compare_roleedge(role)
    else:
        assert len(pysent.getRoles()) == 0

    if opts.get('SYN', False):
        compare_phrase(pysent.getSyntaxTree())
    else:
        assert pysent.getSyntaxTree() is None

    pynouns = pysent.getNouns()
    jnouns = pysent.reference.getNouns()
    for word in pynouns:
        assert type(word) is Word
        assert jnouns.contains(word.reference)

    pynouns = pysent.getModifiers()
    jnouns = pysent.reference.getModifiers()
    for word in pynouns:
        assert type(word) is Word
        assert jnouns.contains(word.reference)

    pynouns = pysent.getVerbs()
    jnouns = pysent.reference.getVerbs()
    for word in pynouns:
        assert type(word) is Word
        assert jnouns.contains(word.reference)

    for word in pysent:
        assert pysent.reference.contains(word.reference)
        compare_words(word, opts)


def test_SentenceSplitter_empty(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ
    sentences = splitter.sentences("")
    assert len(sentences) == 0


def test_SentenceSplitter_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for _, line in EXAMPLES:
        res = splitter(line)
        assert type(res) is list
        assert type(res[0]) is str

        res2 = splitter([line])
        assert len(res) == len(res2) and all(x == y for x, y in zip(res, res2))


def test_Tagger_Sentence_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for cnt, line in EXAMPLES:
        para = tagger(line)
        assert type(para) is list
        for sent in para:
            compare_sentence(sent)

        single = tagger.tagSentence(line)
        assert type(single) is list
        assert len(single) == 1

        compare_sentence(single[0])

        if cnt == 1 and len(para) == 1:
            assert len(para) == len(single)
        else:
            singles = tagger.tagSentence(*[sent.surfaceString() for sent in para])
            assert len(para) == len(singles)


def test_Parser_Syntax_Dep_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for cnt, line in EXAMPLES:
        para = parser(line)
        assert type(para) is list
        for sent in para:
            compare_sentence(sent, {'SYN': True, 'DEP': True})

        singles = parser(*[sent.surfaceString() for sent in para])
        assert len(para) == len(singles)


def test_Parser_Relay_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for _, line in EXAMPLES:
        splits = splitter(line)
        tagged = tagger.tagSentence(*splits)
        assert len(splits) == len(tagged)

        para = parser(tagged)
        assert len(tagged) == len(para)

        assert type(para) is list
        for sent in para:
            compare_sentence(sent, {'SYN': True, 'DEP': True})


def test_RoleLabeler_Role_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for _, line in random.sample(EXAMPLES, 5):
        # 429 Too Many Request를 방지하기 위해 의도적으로 속도를 좀 조절함
        for t in range(random.randint(5, 10)):
            sleep(1)
        para = roleLabeler(line)
        assert type(para) is list
        for sent in para:
            compare_sentence(sent, {'SRL': True, 'NER': True, 'DEP': True, 'WSD': True})


def test_EntityRecog_Entity_typecheck(environ):
    splitter, tagger, parser, entityRecog, roleLabeler = environ

    for _, line in random.sample(EXAMPLES, 5):
        for t in range(random.randint(5, 10)):
            sleep(1)
        para = entityRecog(line)
        for sent in para:
            compare_sentence(sent, {'NER': True, 'WSD': True})
