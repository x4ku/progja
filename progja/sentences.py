import logging
from functools import cache
from random import randint
from . import data, kanji, words


logger = logging.getLogger(__name__)


def random():
    df = load()
    index = randint(0, len(df) - 1)
    return find(df.iloc[index]['Sentence'])


def find(sentence):
    df = load()
    df2 = load_translations()
    compositions = load_compositions()
    progressions = load_progressions()
    df3 = df[df['Sentence'] == sentence]
    records = df3.to_dict('records')
    for record in records:
        df3 = df2[df2['Sentence'] == record['Sentence']]
        record['Translations'] = df3.to_dict('records')
        record['Composition'] = compositions.get(record['Sentence'], [])
        record['Progression'] = progressions.get(record['Sentence'], [])
    return records


@cache
def load():
    logger.info('loading sentences ...')
    df = data.read_csv('sentences', 'sentences.csv') \
        .sort_values(['Sentence']) \
        .reset_index(drop=True)
    logger.info('loaded sentences')
    return df


@cache
def load_translations():
    logger.info('loading sentence translations ...')
    df = data.read_csv('sentences', 'sentence-translations.csv') \
        .sort_values(['Sentence', 'TranslationID']) \
        .reset_index(drop=True)
    logger.info('loaded sentence translations')
    return df


@cache
def count_components():
    logger.info('counting sentence components ...')
    counts = {}
    for composition in load_compositions().values():
        for component in composition:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted sentence components')
    return counts


@cache
def load_compositions():
    logger.info('loading sentence compositions')
    classify = words.component_classifier()
    rows = data.read_json('sentences', 'sentence-compositions.json')
    compositions = {
        row['Sentence']: [
            (component, classify(component) or 'sentence-component')
            for component in row['Composition']
        ]
        for row in rows
    }
    logger.info('loaded sentence compositions')
    return compositions


@cache
def count_progression_components():
    logger.info('counting sentence progression components ...')
    counts = {}
    for progression in load_progressions().values():
        for component in progression:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted sentence progression components')
    return counts


@cache
def load_progressions():
    logger.info('loading sentence progressions ...')
    rows = data.read_json('sentences', 'sentence-progressions.json')
    progressions = {
        row['Sentence']: [tuple(c) for c in row['Progression']]
        for row in rows
    }
    logger.info('loaded sentence progressions')
    return progressions


def progression_builder(
        compositions, kanji_progressions=None, word_progressions=None):
    if not kanji_progressions:
        kanji_progressions = kanji.load_progressions()
    if not word_progressions:
        word_progressions = words.load_progressions()

    def build_progression(root_component):
        # start the progression with the root component
        progression = [root_component]
        # add any kanji components and their progressions
        for character in root_component[0][::-1]:
            if character not in kanji_progressions:
                continue
            # add the kanji component
            component = (character, 'kanji')
            if component in progression:
                progression.remove(component)
            progression.insert(0, component)
            # add components from the kanji's progression
            for component in kanji_progressions[character][::-1]:
                if component in progression:
                    progression.remove(component)
                progression.insert(0, component)
        # add progressions for each subcomponent
        composition = compositions.get(root_component[0], [])
        for component in composition[::-1]:
            # get the component's progression
            components = word_progressions.get(component[0], [component])
            # add new components or move them earlier in the progression
            progression = [c for c in progression if c not in components]
            progression = [*components, *progression]
        return progression
    return build_progression
