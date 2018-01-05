from koalanlp.data import *


def convert_word(result, widx):
    w_length = result.length()
    morphemes = []
    surface = result.surface()

    for i in range(w_length):
        morphs = result.apply(i)
        morpheme = Morpheme(morphs.surface(),
                            morphs.tag().toString(),
                            morphs.rawTag(),
                            i)
        print(morpheme)
        morphemes.append(morpheme)

    word = Word(surface, morphemes, widx)
    dependents = result.deps().toSeq()
    d_length = dependents.size()

    for i in range(d_length):
        rel = dependents.apply(i)
        relationship = Relationship(rel.head(),
                                    rel.relation().toString(),
                                    rel.rawRel(),
                                    rel.target())
        word.dependents.append(relationship)

    return word


def convert_sentence(result):
    s_length = result.length()
    words = []

    for i in range(s_length):
        word = result.apply(i)
        words.append(convert_word(word, i))

    sentence = Sentence(words)
    dependents = result.root().deps().toSeq()
    d_length = dependents.size()

    for i in range(d_length):
        rel = dependents.apply(i)
        relationship = Relationship(rel.head(),
                                    rel.relation().toString(),
                                    rel.rawRel(),
                                    rel.target())
        sentence.root.dependents.append(relationship)

    return sentence


def converter(result):
    p_length = result.size()
    para = []

    for i in range(p_length):
        sentence = result.apply(i)
        para.append(convert_sentence(sentence))

    return para


JString = None


def jstr(s):
    global JString
    if JString is None:
        from jnius import autoclass
        JString = autoclass('java.lang.String')
    return JString(s.encode("UTF-8"))


class Tagger(object):
    def __init__(self, tagger_type):
        from jnius import autoclass
        JTagger = autoclass("kr.bydelta.koala.%s.Tagger" % tagger_type.value)
        self.__tag = JTagger()

    def tag(self, paragraph):
        return converter(self.__tag.tag(jstr(paragraph)))

    def tag_sentence(self, sentence):
        return convert_sentence(self.__tag.tagSentence(jstr(sentence)))


class Parser(object):
    def __init__(self, parser_type, tagger_type=None):
        from jnius import autoclass
        JParser = autoclass("kr.bydelta.koala.%s.Parser" % parser_type.value)
        self.__parse = JParser()
        if not(tagger_type is None):
            JTagger = autoclass("kr.bydelta.koala.%s.Tagger" % tagger_type.value)
            self.__tag = JTagger()
        else:
            self.__tag = None

    def parse(self, paragraph):
        if self.__tag is None:
            return converter(self.__parse.parse(jstr(paragraph)))
        else:
            tagged = self.__tag.tag(jstr(paragraph))
            return converter(self.__parse.parse(tagged))

    def parse_sentence(self, sentence):
        if self.__tag is None:
            return convert_sentence(self.__parse.parseSentence(jstr(sentence)))
        else:
            tagged = self.__tag.tagSentence(jstr(sentence))
            return convert_sentence(self.__parse.parse(tagged))
