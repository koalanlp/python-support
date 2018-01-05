from . import POS


class Morpheme(object):
    def __init__(self, surface, tag, raw_tag, index):
        assert type(surface) is str
        assert type(tag) is str
        assert type(raw_tag) is str
        assert type(index) is int
        self.surface = surface
        self.tag = tag
        self.raw_tag = raw_tag
        self.index = index

    def has_tag(self, tag):
        if type(tag) is str:
            return self.tag.startswith(tag)
        elif type(tag) is list:
            for v in tag:
                if self.tag.startswith(v):
                    return True
            else:
                return False
        else:
            return False

    def has_raw_tag(self, tag):
        if type(tag) is str:
            return self.raw_tag.startswith(tag)
        elif type(tag) is list:
            for v in tag:
                if self.raw_tag.startswith(v):
                    return True
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        if type(other) is Morpheme:
            return other.surface == self.surface and other.tag == self.tag
        else:
            return False

    def equals_without_tag(self, morph):
        if type(morph) is Morpheme:
            return morph.surface == self.surface
        else:
            return False

    def __repr__(self):
        return "%s/%s(%s)" % (self.surface, self.tag, self.raw_tag)

    def to_dict(self):
        return {
            "surface": self.surface,
            "tag": self.tag,
            "rawTag": self.tag
        }


class Relationship(object):
    def __init__(self, head, relation, raw_rel, target):
        assert type(head) is int
        assert type(relation) is str
        assert type(raw_rel) is str
        assert type(target) is int

        self.head = head
        self.relation = relation
        self.raw_rel = raw_rel
        self.target = target

    def __eq__(self, other):
        if type(other) is Relationship:
            return self.head == other.head and self.relation == other.relation and self.target == other.target
        else:
            return False

    def __repr__(self):
        return "Rel:%s (ID:%s → ID:%s)" % (self.relation, self.head, self.target)

    def to_dict(self):
        return {
            "head_id": self.head,
            "target_id": self.target,
            "relation": self.relation,
            "raw_rel": self.raw_rel
        }


class Word(object):
    def __init__(self, surface=None, morphemes=None, index=None):
        if surface is None:
            self.surface = "##ROOT##"
            self.morphemes = []
            self.index = -1
        else:
            assert type(surface) is str
            assert type(morphemes) is list, type(morphemes[0]) is Morpheme
            assert type(index) is int

            self.surface = surface
            self.morphemes = morphemes
            self.index = index

        self.dependents = []

    def __len__(self):
        return len(self.morphemes)

    def __getitem__(self, item):
        return self.morphemes[item]

    def __iter__(self):
        return iter(self.morphemes)

    def matches(self, tag):
        if type(tag) is list:
            tag_list = tag
            for m in self.morphemes:
                if len(tag_list) > 0 and m.tag.startswith(tag_list[0]):
                    tag_list.remove(0)
            return len(tag_list) == 0
        else:
            return False

    def find(self, fn):
        if callable(fn):
            for m in self.morphemes:
                if fn(m):
                    return m
            else:
                return None
        elif type(fn) is Morpheme:
            for m in self.morphemes:
                if m == fn:
                    return m
            else:
                return None
        else:
            return None

    def __contains__(self, item):
        return not(self.find(item) is None)

    def exists(self, fn):
        return self.__contains__(fn)

    def equals_without_tag(self, another):
        if type(another) is Word:
            return another.surface == self.surface
        else:
            return False

    def __eq__(self, other):
        if type(other) is Word:
            is_equal = other.id == self.index and len(self) == len(other)
            for i in range(len(self)):
                is_equal = is_equal and self[i] == other[i]
            return is_equal
        else:
            return False

    def __repr__(self):
        morph_str = "+".join([str(m) for m in self.morphemes])
        repr_str = "%s\t= %s" % (self.surface, morph_str)
        if len(self.dependents) > 0:
            for r in self.dependents:
                repr_str += "\n.... 이 어절의 %s: 어절 [#%s]" % (r.relation, r.target)
        return repr_str

    def single_line_string(self):
        repr_str = ["%s/%s" % (m.surface, m.tag) for m in self.morphemes]
        return "+".join(repr_str)

    def to_dict(self):
        return {
            "surface": self.surface,
            "morphemes": [m.to_dict() for m in self.morphemes],
            "dependents": [r.to_dict() for r in self.dependents]
        }


class Sentence(object):
    def __init__(self, words):
        assert type(words) is list, type(words[0]) is Word
        self.words = words
        self.root = Word()

    def matches(self, tag):
        if type(tag) is list:
            tag_list = tag
            for w in self.words:
                if len(tag_list) > 0 and w.matches(tag_list[0]):
                    tag_list.remove(0)
            return len(tag_list) == 0
        else:
            return False

    def find(self, fn):
        if callable(fn):
            for m in self.words:
                if fn(m):
                    return m
            else:
                return None
        elif type(fn) is Word:
            for m in self.words:
                if m == fn:
                    return m
            else:
                return None
        else:
            return None

    def __contains__(self, item):
        return not(self.find(item) is None)

    def exists(self, fn):
        return self.__contains__(fn)

    def nouns(self):
        return [w for w in self.words if w.exists(POS.is_noun)]

    def verbs(self):
        return [w for w in self.words if w.exists(POS.is_predicate)]

    def modifiers(self):
        return [w for w in self.words if w.exists(POS.is_modifier)]

    def __getitem__(self, item):
        return self.words[item]

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return iter(self.words)

    def __repr__(self):
        repr_str = self.surface_string() + "\n"
        for w in self.words:
            repr_str += "[#%s] %s" % (w.index, str(w))
            is_root = len([r for r in self.root.dependents if r.target == w.index])
            if is_root > 0:
                repr_str += "\n.... 이 어절이 ROOT 입니다"
            repr_str += "\n"
        return repr_str

    def surface_string(self, delimiter=" "):
        return delimiter.join([w.surface for w in self.words])

    def single_line_string(self):
        return " ".join([w.single_line_string() for w in self.words])

    def to_dict(self):
        return {
            "words": [m.to_dict() for m in self.words],
            "root": [r.to_dict() for r in self.root.dependents]
        }
