import unittest
import progja


class TestDecks(unittest.TestCase):

    def test_create_sentence_reading(self):
        reading = ' '.join([
            'あなた',
            'が',
            '行か【イカ】',
            'ない',
            'の',
            'なら',
            '、',
            '僕【ボク】',
            'も',
            '行か【イカ】',
            'ない',
            '。'
        ])
        expected = ' '.join([
            'あなた',
            'が',
            '行か<span class="reading">【イカ】</span>',
            'ない',
            'の',
            'なら',
            '、',
            '僕<span class="reading">【ボク】</span>',
            'も',
            '行か<span class="reading">【イカ】</span>',
            'ない',
            '。'
        ])
        actual = progja.decks.create_sentence_reading(reading)
        self.assertEqual(actual, expected)
