import re
import unittest
import progja


class TestKanji(unittest.TestCase):

    pass


class TestKanjiCompositions(unittest.TestCase):

    def setUp(self):
        self.df = progja.kanji.load()
        self.kanji = set(self.df['Kanji'])
        self.compositions = progja.kanji.load_compositions()
        self.components = {
            component
            for kanji, composition in self.compositions.items()
            for component in composition
        }
        self.variants = {c[0] for c in self.components if len(c[0]) > 1}

    def test_root_components_are_kanji(self):
        for component in self.components:
            message = '{} root is not a kanji'.format(component[0])
            self.assertTrue(component[0][0] in self.kanji, message)

    def test_variants_match_valid_pattern(self):
        pattern = re.compile('^.\(.\)$')
        for variant in self.variants:
            message = '{} is an invalid variant pattern'.format(variant)
            self.assertRegex(variant, pattern, message)

    def test_variants_do_not_occur_alone(self):
        for variant in self.variants:
            if len(variant) < 3:
                continue
            message = '{} of {} cannot occur alone'.format(variant[2], variant)
            self.assertFalse(variant[2] in self.components, message)


class TestKanjiProgressions(unittest.TestCase):

    def setUp(self):
        self.progressions = progja.kanji.load_progressions()

    def test_progression_contains_at_least_one_component(self):
        for root, progression in self.progressions.items():
            message = '{} progression is empty'.format(root)
            self.assertGreater(len(progression), 0, message)

    def test_last_component_in_progression_is_root(self):
        for root, progression in self.progressions.items():
            for i in range(-1, -1 * len(progression), -1):
                tail = progression[i]
                message = ('{} progression tail component {} is not root or '
                    'root variant'.format(root, tail[0]))
                self.assertEqual(tail[0][0], root, message)
                if tail[0] == root:
                    break
