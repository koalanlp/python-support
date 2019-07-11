from koalanlp import Util
from koalanlp.data import *
from koalanlp.types import *
import pytest

sent = None
sent2 = None
sent3 = None
sent4 = None


@pytest.fixture(scope="session")
def jvm():
    Util.initialize()
    yield None
    Util.finalize()


def set_sentence():
    global sent, sent2, sent3, sent4

    sent = Sentence([
        Word("나는", [
            Morpheme("나", POS.NP, "NP"),
            Morpheme("는", POS.JX, "JX")
        ]),
        Word("밥을", [
            Morpheme("밥", POS.NNG, "NNG"),
            Morpheme("을", POS.JKO, "JKO")
        ])
    ])

    sent2 = Sentence([
        Word("흰", [
            Morpheme("희", POS.VA, "VA"),
            Morpheme("ㄴ", POS.ETM, "ETM")
        ]),
        Word("밥을", [
            Morpheme("밥", POS.NNG, "NNG"),
            Morpheme("을", POS.JKO, "JKO")
        ]),
        Word("나는", [
            Morpheme("나", POS.NP, "NP"),
            Morpheme("는", POS.JX, "JX")
        ]),
        Word("먹었다", [
            Morpheme("먹", POS.VV, "VV"),
            Morpheme("었", POS.EP, "EP"),
            Morpheme("다", POS.EF, "EF")
        ])
    ])

    sent3 = Sentence([
        Word("흰", [
            Morpheme("희", POS.VA, "VA"),
            Morpheme("ㄴ", POS.ETM, "ETM")
        ]),
        Word("밥을", [
            Morpheme("밥", POS.NNG, "NNG"),
            Morpheme("을", POS.JKO, "JKO")
        ]),
        Word("나는", [
            Morpheme("나", POS.NP, "NP"),
            Morpheme("는", POS.JX, "JX")
        ]),
        Word("먹었다", [
            Morpheme("먹", POS.VV, "VV"),
            Morpheme("었", POS.EP, "EP"),
            Morpheme("다", POS.EF, "EF")
        ])
    ])

    sent4 = Sentence([
        Word("칠한", [
            Morpheme("칠", POS.NNG, "NN"),
            Morpheme("하", POS.XSV, "XSV"),
            Morpheme("ㄴ", POS.ETM, "ETM")
        ]),
        Word("밥을", [
            Morpheme("밥", POS.NNG, "NNG"),
            Morpheme("을", POS.JKO, "JKO")
        ]),
        Word("너는", [
            Morpheme("너", POS.NP, "NP"),
            Morpheme("는", POS.JX, "JX")
        ]),
        Word("먹음", [
            Morpheme("먹", POS.VV, "VV"),
            Morpheme("음", POS.ETN, "ETN")
        ])
    ])


def test_Morpheme(jvm):
    dummy1 = None
    dummy2 = None
    unknown = None

    def reset():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = Morpheme("밥", POS.NNP, "NNP")
        dummy2 = Morpheme("밥", POS.NNG, "ncn")
        unknown = Morpheme("??", POS.NA)

    def check_id():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.id is None
        assert dummy2.id is None

        # The ID can be set initially.
        dummy1.id = 5
        assert dummy1.id == 5

        # After initializing id, it cannot be modified.
        try:
            dummy1.id = 7
            raise AssertionError()
        except AssertionError as e:
            # propagate error
            raise e
        except Exception:
            pass

        try:
            sent[0][1].id = 8
            raise AssertionError()
        except AssertionError as e:
            # propagate error
            raise e
        except Exception:
            pass

        for word in sent2:
            for index, morpheme in enumerate(word):
                assert morpheme.id == index

    def check_surface():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.surface == '밥'
        assert dummy2.surface == '밥'

    def check_tag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.getTag() == POS.NNP
        assert dummy2.getTag() == POS.NNG

    def check_original_tag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.originalTag == "NNP"
        assert dummy2.originalTag == 'ncn'

    def check_wordsense():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        # Expect not to throw an error
        dummy1.wordSense = 1
        dummy2.wordSense = 2

        assert sent2[0][0].getWordSense() is None
        assert dummy1.getWordSense() == 1
        assert dummy2.getWordSense() == 2

    def check_noun():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.isNoun()
        assert dummy2.isNoun()
        assert not unknown.isNoun()

    def check_verb():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert not dummy1.isPredicate()
        assert not dummy2.isPredicate()
        assert not unknown.isPredicate()

    def check_modifier():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert not dummy1.isModifier()
        assert not dummy2.isModifier()
        assert not unknown.isModifier()

    def check_josa():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert not dummy1.isJosa()
        assert not dummy2.isJosa()
        assert not unknown.isJosa()

    def check_hastag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.hasTag("N")
        assert not dummy1.hasTag("V")

        assert not unknown.hasTag("N")
        assert unknown.hasTag("NA")

    def check_hasoneoftag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.hasTagOneOf("N", "V")
        assert not dummy1.hasTagOneOf("V", "E")

        assert not unknown.hasTagOneOf("NN", "NP")
        assert unknown.hasTagOneOf("NA", "NN")

    def check_hasoriginaltag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.hasOriginalTag("NN")
        assert dummy1.hasOriginalTag("nn")
        assert not dummy1.hasOriginalTag("nc")

        assert dummy2.hasOriginalTag("NC")
        assert dummy2.hasOriginalTag("nc")
        assert not dummy2.hasOriginalTag("NN")

        assert not unknown.hasOriginalTag("NA")

    def check_equal():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1 == dummy1

        assert not dummy1 == dummy2
        assert not dummy2 == dummy1

        assert dummy2 == sent2[1][0]
        assert sent2[1][0] == dummy2

        assert dummy2 == sent[1][0]
        assert sent[1][0] == sent2[1][0]

        assert dummy1 != unknown
        assert dummy1 != 1

    def check_equalswithouttag():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert dummy1.equalsWithoutTag(dummy2)
        assert not dummy2.equalsWithoutTag(unknown)

    def check_stringrepr():
        global dummy1, dummy2, unknown
        global sent, sent2, sent3, sent4

        assert str(dummy1) == "밥/NNP(NNP)"
        assert str(dummy2) == "밥/NNG(ncn)"
        assert str(unknown) == "??/NA"

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_Word(jvm):
    dummy1 = None
    dummy2 = None

    def reset():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = Word("밥을", [
            Morpheme("밥", POS.NNG, "NNG"),
            Morpheme("을", POS.JKO, "JKO")
        ])

        dummy2 = Word("밥을", [
            Morpheme("밥", POS.NNP),
            Morpheme("을", POS.NNP)
        ])

    def check_id():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.id is None

        # The ID can be set initially.
        dummy1.id = 5
        assert dummy1.id == 5

        for index, word in enumerate(sent2):
            assert word.id == index

    def check_surface():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.surface == '밥을'
        assert sent[0].surface == '나는'

    def check_list_access():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1[0] == Morpheme("밥", POS.NNG)
        assert dummy1[1] == Morpheme("을", POS.JKO)

    def check_list_index():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.index(dummy1[0]) == 0
        assert dummy1.index(dummy1[1]) == 1

        assert dummy1.index(Morpheme("밥", POS.NNG)) == 0
        assert dummy1.index(Morpheme("을", POS.JKO)) == 1

        assert dummy1[0] in dummy1
        assert Morpheme("밥", POS.NNP) not in dummy1
        assert Morpheme("밥", POS.NNG) in dummy1
        assert Morpheme("밥", POS.NNP) not in dummy1

    def check_properties():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert len(dummy1.getEntities()) == 0
        assert dummy1.getPhrase() is None
        assert len(dummy1.getArgumentRoles()) == 0
        assert len(dummy1.getPredicateRoles()) == 0
        assert len(dummy1.getDependentEdges()) == 0
        assert dummy1.getGovernorEdge() is None

        # All these trees automatically set pointers on the words
        Entity("밥", CoarseEntityType.PS, "PS_OTHER", [dummy1[0]])
        Entity("밥", CoarseEntityType.PS, "PS_SOME", [dummy1[0]])
        Entity("밥", CoarseEntityType.PS, "PS_ANOTHER", [dummy1[0]])

        tree = SyntaxTree(PhraseTag.NP, dummy1)
        dep = DepEdge(dummy1, dummy2, PhraseTag.NP, DependencyTag.SBJ)
        role = RoleEdge(dummy1, dummy2, RoleType.ARG0)

        assert len(dummy1.getEntities()) != 0
        assert "PS_OTHER" in [it.fineLabel for it in dummy1.getEntities()]
        assert dummy1.getPhrase() == tree
        assert dummy1.getArgumentRoles()[0] == role
        assert dummy2.getPredicateRoles()[0] == role
        assert dummy1.getDependentEdges()[0] == dep
        assert dummy2.getGovernorEdge() == dep

    def check_equal():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1
        # Symmetry
        assert dummy1 != dummy2
        assert dummy2 != dummy1

        assert dummy1 == sent[1]
        assert sent[1] == dummy1

        assert dummy1[0].getWord() == dummy1
        assert dummy2[0].getWord() == dummy2

        assert dummy1 != dummy1[0]
        assert sum(1 for it in sent if it == dummy1) == 1
        assert sum(1 for it in sent2 if it == dummy1) == 1

        assert dummy1 != dummy1[0]

    def check_equalswithouttag():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.equalsWithoutTag(dummy2)
        assert not dummy2.equalsWithoutTag(sent[0])

    def check_stringrepr():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert str(dummy1) == "밥을 = 밥/NNG+을/JKO"
        assert str(dummy2) == "밥을 = 밥/NNP+을/NNP"

    def check_singlelinestr():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.singleLineString() == "밥/NNG+을/JKO"
        assert dummy2.singleLineString() == "밥/NNP+을/NNP"

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_Sentence(jvm):
    def reset():
        set_sentence()

    def check_accessmorphme():
        global sent, sent2, sent3, sent4

        assert sent[0].surface == '나는'
        assert sent[1].surface == '밥을'

    def check_indexofmorph():
        global sent, sent2, sent3, sent4

        assert sent.index(sent[0]) == 0
        assert sent.index(sent[1]) == 1

        assert sent2.index(sent[0]) == 2
        assert sent2.index(sent[1]) == 1

        assert sent[0] in sent
        assert sent[1] in sent
        assert sent2[0] not in sent
        assert sent2[1] in sent

    def check_property():
        global sent, sent2, sent3, sent4

        assert len(sent.getCorefGroups()) == 0
        assert len(sent.getEntities()) == 0
        assert sent.getSyntaxTree() is None
        assert len(sent.getDependencies()) == 0
        assert len(sent.getRoles()) == 0

        sent.entities = [Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=[sent[0][0]]
        )]
        sent.corefGroups = [CoreferenceGroup([sent.getEntities()[0]])]
        sent.syntaxTree = SyntaxTree(
            label=PhraseTag.S, children=[
                SyntaxTree(label=PhraseTag.NP, terminal=sent[0]),
                SyntaxTree(label=PhraseTag.NP, terminal=sent[1])
            ]
        )
        sent.dependencies = [
            DepEdge(dependent=sent[1], type=PhraseTag.S, depType=DependencyTag.ROOT),
            DepEdge(governor=sent[1], dependent=sent[0], type=PhraseTag.S, depType=DependencyTag.ROOT)
        ]
        sent.roles = [
            RoleEdge(predicate=sent[1], argument=sent[0], label=RoleType.ARG0)
        ]

        assert sent.getCorefGroups()[0][0] == sent.getEntities()[0]
        assert sent.getEntities()[0].fineLabel == "PS_OTHER"
        assert sent.getSyntaxTree().getLabel() == PhraseTag.S
        assert sent.getDependencies()[0].getDepType() == DependencyTag.ROOT
        assert sent.getRoles()[0].getLabel() == RoleType.ARG0

    def check_nounlist():
        global sent, sent2, sent3, sent4

        assert sent2.getNouns() == sent2[1:3]
        assert sent4.getNouns() == sent4[1:4]

    def check_verblist():
        global sent, sent2, sent3, sent4

        assert sent2.getVerbs() == [sent2[3]]
        assert len(sent4.getVerbs()) == 0

    def check_modlist():
        global sent, sent2, sent3, sent4

        assert sent2.getModifiers() == [sent2[0]]
        assert sent4.getModifiers() == [sent4[0]]

    def check_stringrepr():
        global sent, sent2, sent3, sent4

        assert str(sent) == "나는 밥을"
        assert str(sent2) == "흰 밥을 나는 먹었다"

        assert str(sent) == sent.surfaceString()
        assert str(sent2) == sent2.surfaceString()

        assert sent.surfaceString("/") == "나는/밥을"
        assert sent2.surfaceString("/") == "흰/밥을/나는/먹었다"

    def check_singlelinestring():
        global sent, sent2, sent3, sent4

        assert sent.singleLineString() == "나/NP+는/JX 밥/NNG+을/JKO"
        assert sent2.singleLineString() == "희/VA+ㄴ/ETM 밥/NNG+을/JKO 나/NP+는/JX 먹/VV+었/EP+다/EF"

    def check_equal():
        global sent, sent2, sent3, sent4

        # Reflexive
        assert sent2 == sent2

        # Symmetry
        assert sent != sent2
        assert sent2 != sent4

        assert sent2 == sent3
        assert sent3 == sent2

        assert sent != sent[0]

    def check_reference_build():
        global sent, sent2, sent3, sent4

        reference = sent.getReference()
        by_reference = Sentence.fromJava(reference)

        assert by_reference == sent

        for reconword, word in zip(by_reference, sent):
            refword = reference.get(word.id)

            assert reconword.id == word.id
            assert refword.getId() == word.id

            for reconmorph, morph in zip(reconword, word):
                refmorph = refword.get(morph.id)

                assert reconmorph.id == morph.id
                assert refmorph.getId() == morph.id

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_SyntaxTree(jvm):
    dummy1 = None
    dummy2 = None

    def reset():
        global dummy1, dummy2

        set_sentence()

        dummy1 = SyntaxTree(
            label=PhraseTag.S,
            children=[
                SyntaxTree(
                    label=PhraseTag.NP, children=[
                        SyntaxTree(label=PhraseTag.DP, terminal=sent2[0], originalLabel="DP"),
                        SyntaxTree(label=PhraseTag.NP, terminal=sent2[1], originalLabel="NP")
                    ]
                ),
                SyntaxTree(
                    label=PhraseTag.VP, children=[
                        SyntaxTree(label=PhraseTag.NP, terminal=sent2[2]),
                        SyntaxTree(label=PhraseTag.VP, terminal=sent2[3])
                    ]
                )
            ]
        )

        dummy2 = SyntaxTree(
            label=PhraseTag.S,
            children=[
                SyntaxTree(
                    label=PhraseTag.NP, children=[
                        SyntaxTree(label=PhraseTag.DP, terminal=sent3[0], originalLabel="dp"),
                        SyntaxTree(label=PhraseTag.NP, terminal=sent3[1], originalLabel="np")
                    ]
                ),
                SyntaxTree(
                    label=PhraseTag.VP, children=[
                        SyntaxTree(label=PhraseTag.NP, terminal=sent3[2]),
                        SyntaxTree(label=PhraseTag.VP, terminal=sent3[3])
                    ]
                )
            ]
        )

    def check_childaccess():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1[0].getLabel() == PhraseTag.NP
        assert dummy1[1].getLabel() == PhraseTag.VP
        assert dummy1[0][0].getLabel() == PhraseTag.DP

        assert dummy1[0][0].originalLabel == "DP"
        assert dummy1[0][1].originalLabel == "NP"
        assert dummy2[0][0].originalLabel == "dp"
        assert dummy2[0][1].originalLabel == "np"
        assert dummy1[0].originalLabel is None

        assert dummy1[0].hasNonTerminals()
        assert not dummy1[0][0].hasNonTerminals()

    def check_parentaccess():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.isRoot()
        assert not dummy1[0].isRoot()
        assert not dummy1[0][0].isRoot()

        assert dummy1[0].getParent() == dummy1
        assert dummy1[0][0].getParent() == dummy1[0]
        assert dummy1[0][1].getParent() == dummy1[0]

    def check_terminalaccess():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.getTerminals() == list(sent2)
        assert dummy1[0].getTerminals() == sent2[0:2]
        assert dummy1[1].getTerminals() == [sent2[2], sent2[3]]
        assert dummy1[0][0].getTerminals() == [sent2[0]]

    def check_equal():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1
        assert list(dummy1) == list(dummy1.getNonTerminals())

        # Symmetry
        assert dummy1 == dummy2
        assert dummy2 == dummy1

        assert dummy1 != dummy1[0]
        assert dummy1[0] != dummy1[1]
        assert dummy1 != sent2[0]

    def check_index():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.index(dummy1[0]) == 0
        assert dummy1.index(dummy1[1]) == 1

        assert dummy1.index(dummy2[0]) == 0
        assert dummy1.index(dummy2[1]) == 1

        assert dummy1[0] in dummy1
        assert dummy1[0][1] not in dummy1
        assert dummy2[0] in dummy1
        assert dummy2[0][1] not in dummy1

    def check_stringrepr():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert str(dummy1) == "S-Node()"
        assert str(dummy1[0]) == "NP-Node()"
        assert str(dummy1[0][0]) == "DP-Node(흰 = 희/VA+ㄴ/ETM)"

    def check_treerepr():
        global dummy1, dummy2
        global sent, sent2, sent3, sent4

        assert dummy1.getTreeString() == """
S-Node()
| NP-Node()
| | DP-Node(흰 = 희/VA+ㄴ/ETM)
| | NP-Node(밥을 = 밥/NNG+을/JKO)
| VP-Node()
| | NP-Node(나는 = 나/NP+는/JX)
| | VP-Node(먹었다 = 먹/VV+었/EP+다/EF) 
        """.strip()

        assert dummy1[0].getTreeString() == """
NP-Node()
| DP-Node(흰 = 희/VA+ㄴ/ETM)
| NP-Node(밥을 = 밥/NNG+을/JKO)
        """.strip()

    def check_info():
        global dummy1, dummy2

        assert dummy1.getLabel() == PhraseTag.S

        assert dummy1.terminal is None
        assert dummy1[0].terminal is None
        assert dummy1[0][0].terminal == sent2[0]

    def check_reference():
        global dummy1, dummy2

        sent2.syntaxTree = dummy1
        reference = sent2.getReference()
        by_reference = Sentence.fromJava(reference)
        print(by_reference.getSyntaxTree().getTreeString())

        assert by_reference.getSyntaxTree() == sent2.getSyntaxTree()

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_DepEdge(jvm):
    dummy1 = None
    dummy2 = None
    dummy3 = None
    dummy4 = None
    dummy5 = None

    def reset():
        global dummy1, dummy2, dummy3, dummy4, dummy5
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = DepEdge(
            governor=sent2[3],
            dependent=sent2[1],
            type=PhraseTag.NP,
            depType=DependencyTag.OBJ
        )
        dummy2 = DepEdge(
            governor=sent3[3],
            dependent=sent3[1],
            type=PhraseTag.NP,
            depType=DependencyTag.OBJ,
            originalLabel="NPobj"
        )
        dummy3 = DepEdge(
            governor=sent3[3],
            dependent=sent3[2],
            type=PhraseTag.NP,
            depType=DependencyTag.SBJ
        )
        dummy4 = DepEdge(governor=sent3[1], dependent=sent3[0], type=PhraseTag.DP)
        dummy5 = DepEdge(dependent=sent3[3], type=PhraseTag.VP, depType=DependencyTag.ROOT)

    def check_property():
        global dummy1, dummy2, dummy3, dummy4, dummy5
        global sent, sent2, sent3, sent4

        assert dummy1.src == sent2[3]
        assert dummy1.governor == dummy1.src

        assert dummy1.dest == sent2[1]
        assert dummy1.dependent == dummy1.dest

        assert dummy1.getType() == PhraseTag.NP
        assert dummy1.getDepType() == DependencyTag.OBJ
        assert dummy1.getLabel() == DependencyTag.OBJ

        assert dummy1.originalLabel is None
        assert dummy2.originalLabel == "NPobj"

    def check_stringrepr():
        global dummy1, dummy2, dummy3, dummy4, dummy5
        global sent, sent2, sent3, sent4

        assert str(dummy1) == "NPOBJ('먹었다 = 먹/VV+었/EP+다/EF' → '밥을 = 밥/NNG+을/JKO')"
        assert str(dummy3) == "NPSBJ('먹었다 = 먹/VV+었/EP+다/EF' → '나는 = 나/NP+는/JX')"
        assert str(dummy4) == "DP('밥을 = 밥/NNG+을/JKO' → '흰 = 희/VA+ㄴ/ETM')"
        assert str(dummy5) == "VPROOT('ROOT' → '먹었다 = 먹/VV+었/EP+다/EF')"

    def check_equal():
        global dummy1, dummy2, dummy3, dummy4, dummy5
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1

        # Symmetry
        assert dummy1 == dummy2
        assert dummy2 == dummy1

        assert dummy1 != dummy3
        assert dummy1 != dummy4
        assert dummy1 != dummy1.src

    def check_reference():
        global dummy1, dummy2, dummy3, dummy4, dummy5

        sent2.dependencies = [dummy1]
        reference = sent2.getReference()
        assert reference.getDependencies().size() > 0

        by_reference = Sentence.fromJava(reference)
        assert by_reference.getDependencies() == sent2.getDependencies()

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_RoleEdge(jvm):
    dummy1 = None
    dummy2 = None
    dummy3 = None
    dummy4 = None

    def reset():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = RoleEdge(
            predicate=sent2[3],
            argument=sent2[1],
            label=RoleType.ARG1,
            modifiers=[sent2[0]]
        )
        dummy2 = RoleEdge(
            predicate=sent3[3],
            argument=sent3[1],
            label=RoleType.ARG1,
            originalLabel="ARG-1"
        )
        dummy3 = RoleEdge(predicate=sent3[3], argument=sent3[2], label=RoleType.ARG0)
        dummy4 = RoleEdge(predicate=sent3[1], argument=sent3[0], label=RoleType.ARGM_PRD)

    def check_property():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        assert dummy1.src == sent2[3]
        assert dummy1.predicate == dummy1.src

        assert dummy1.dest == sent2[1]
        assert dummy1.argument == dummy1.dest

        assert dummy1.getLabel() == RoleType.ARG1

        assert dummy1.modifiers[0] == sent2[0]

        assert dummy1.originalLabel is None
        assert dummy2.originalLabel == "ARG-1"

    def check_stringrepr():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        assert str(dummy1) == "ARG1('먹었다' → '밥을/흰')"
        assert str(dummy3) == "ARG0('먹었다' → '나는/')"
        assert str(dummy4) == "ARGM_PRD('밥을' → '흰/')"

    def check_equal():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1

        # Symmetry
        assert dummy1 == dummy2
        assert dummy2 == dummy1

        assert dummy1 != dummy3
        assert dummy1 != dummy4
        assert dummy1 != dummy1.src

    def check_reference():
        global dummy1, dummy2, dummy3, dummy4

        sent2.roles = [dummy1]
        reference = sent2.getReference()
        assert reference.getRoles().size() > 0

        by_reference = Sentence.fromJava(reference)
        assert by_reference.getRoles() == sent2.getRoles()

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_Entity(jvm):
    dummy1 = None
    dummy2 = None
    dummy3 = None
    dummy4 = None

    def reset():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=[sent3[2][0]]
        )
        dummy2 = Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=[sent3[2][0]]
        )
        dummy3 = Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_DIFF",
            morphemes=[sent3[2][0]]
        )
        dummy4 = Entity(
            surface="흰 밥",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=list(sent3[0]) + list(sent3[1])
        )

    def check_property():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        assert dummy1.getLabel() == CoarseEntityType.PS
        assert dummy1.fineLabel == "PS_OTHER"
        assert dummy1[0] == sent3[2][0]

        assert dummy1.surface == "나"
        assert dummy4.surface == "흰 밥"

        assert sent3[2][0] in dummy1
        assert sent3[1][0] not in dummy1

        assert dummy1.getCorefGroup() is None

    def check_equal():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1

        # Symmetry
        assert dummy1 == dummy2
        assert dummy2 == dummy1

        assert dummy1 != dummy3
        assert dummy1 != dummy4
        assert dummy1 != dummy1[0]

    def check_reference():
        global dummy1, dummy2, dummy3, dummy4

        sent3.entities = [dummy1, dummy2, dummy3, dummy4]
        reference = sent3.getReference()
        assert reference.getEntities().size() > 0

        by_reference = Sentence.fromJava(reference)
        assert by_reference.getEntities() == sent3.getEntities()

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()


def test_CorefGroup(jvm):
    dummy1 = None
    dummy2 = None
    dummy3 = None
    dummy4 = None

    def reset():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4
        set_sentence()

        dummy1 = CoreferenceGroup([Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=[sent3[2][0]]
        )])
        dummy2 = CoreferenceGroup([Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes=[sent3[2][0]]
        )])
        dummy3 = CoreferenceGroup([Entity(
            surface="나",
            label=CoarseEntityType.PS,
            fineLabel="PS_DIFF",
            morphemes=[sent3[2][0]]
        )])
        dummy4 = CoreferenceGroup([Entity(
            surface="흰 밥",
            label=CoarseEntityType.PS,
            fineLabel="PS_OTHER",
            morphemes= list(sent3[0]) + list(sent3[1])
        )])


    def check_list_inherit():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        assert dummy1[0] in dummy1
        assert dummy3[0] not in dummy1
        assert dummy1.index(dummy1[0]) == 0

    def check_equal():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        # Reflexive
        assert dummy1 == dummy1

        # Symmetry
        assert dummy1 == dummy2
        assert dummy2 == dummy1

        assert dummy1 != dummy3
        assert dummy1 != dummy4
        assert dummy1 != dummy1[0]

        assert dummy1[0].getCorefGroup() == dummy1
        assert dummy1[0].getCorefGroup() == dummy2

    def check_reference():
        global dummy1, dummy2, dummy3, dummy4
        global sent, sent2, sent3, sent4

        sent3.entities = [dummy1[0], dummy3[0], dummy4[0]]
        sent3.corefGroups = [dummy1, dummy3, dummy4]
        reference = sent3.getReference()
        assert reference.getEntities().size() > 0

        by_reference = Sentence.fromJava(reference)
        assert by_reference.getCorefGroups() == sent3.getCorefGroups()

    for name, method in locals().items():
        if name.startswith('check_'):
            reset()
            method()
