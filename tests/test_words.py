import unittest
import progja


class TestWords(unittest.TestCase):

    pass


class TestWordCompositions(unittest.TestCase):

    pass


class TestWordProgressions(unittest.TestCase):

    def setUp(self):
        self.progressions = progja.words.load_progressions()

    def test_progression_contains_at_least_one_component(self):
        for root, progression in self.progressions.items():
            message = '{} progression is empty'.format(root)
            self.assertGreater(len(progression), 0, message)

    def test_last_component_in_progression_is_root(self):
        for root, progression in self.progressions.items():
            tail = progression[-1]
            message = ('{} progression tail component {} is not root'
                .format(root, tail[0]))
            self.assertEqual(tail[0], root, message)
