import logging
from functools import cache
from random import randint
import pandas as pd
from . import data, kanji


logger = logging.getLogger(__name__)


def random(common=False, uncommon=False):
    df = (
        load_common() if common
        else load_uncommon() if uncommon
        else load()
    )
    index = randint(0, len(df) - 1)
    word = df.iloc[index]
    return find(word['Word'], word['Reading'])


def find_common_or_any(word=None, reading=None):
    return (
        find_common(word, reading)
        or find(word, reading)
    )


def find_common(word=None, reading=None):
    return find(word, reading, common=True)


def find(word=None, reading=None, common=None):
    df1 = load_common() if common else load()
    df2 = load_common_sometimes_kana() if common else load_sometimes_kana()
    df3 = load_common_definitions() if common else load_definitions()
    compositions = load_compositions()
    progressions = load_progressions()
    df4 = df1
    if word:
        df4 = df4[df1['Word'] == word]
        if len(df4) == 0:
            df4 = df2[df2['Reading'] == word]
    if reading:
        df4 = df4[df4['Reading'] == reading]
    records = df4.to_dict('records')
    for record in records:
        df5 = df3[df3['Word'] == record['Word']]
        df5 = df5[df5['Reading'] == record['Reading']]
        record['Definitions'] = df5.to_dict('records')
        record['Composition'] = compositions.get(record['Word'], [])
        record['Progression'] = progressions.get(record['Word'], [])
    return records


@cache
def load_sometimes_kana():
    logger.info('loading words sometimes written in kana ...')
    dfs = [load_common_sometimes_kana(), load_uncommon_sometimes_kana()]
    sort_by = ['Word', 'Reading']
    df = pd.concat(dfs).sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded words sometimes written in kana')
    return df


@cache
def load_common_sometimes_kana():
    logger.info('loading common words sometimes written in kana ...')
    df = load_common()
    mask = df['IsSometimesKana']
    sort_by = ['Word', 'Reading']
    df = df[mask].sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded common words sometimes written in kana')
    return df


@cache
def load_uncommon_sometimes_kana():
    logger.info('loading uncommon words sometimes written in kana ...')
    df = load_uncommon()
    mask = df['IsSometimesKana']
    sort_by = ['Word', 'Reading']
    df = df[mask].sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded uncommon words sometimes written in kana')
    return df


@cache
def load():
    logger.info('loading words ...')
    dfs = [load_common(), load_uncommon()]
    sort_by = ['Word', 'Reading']
    df = pd.concat(dfs).sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded words')
    return df


@cache
def load_common():
    logger.info('loading common words ...')
    filename = 'words-common.csv'
    df = data.load_csv(filename)
    copy = df.copy()
    copy['_PriorityCount'] = (
        (copy['PriorityNF'] > 0).astype(int)
        + (copy['PriorityIchi'] > 0).astype(int)
        + (copy['PriorityNews'] > 0).astype(int)
    )
    sort_by = ['_PriorityCount', 'PriorityNF', 'PriorityIchi', 'PriorityNews',
        'Word', 'Reading']
    sort_ascending = [0, 1, 1, 1, 1, 1]
    sort_index = copy.sort_values(sort_by, ascending=sort_ascending).index
    df = df.reindex(sort_index).reset_index(drop=True)
    logger.info('loaded common words')
    return df


@cache
def load_uncommon():
    logger.info('loading uncommon words ...')
    filename = 'words-uncommon.csv'
    sort_by = ['Word', 'Reading']
    df = data.load_csv(filename).sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded uncommon words')
    return df


@cache
def load_definitions():
    logger.info('loading word definitions ...')
    dfs = [load_common_definitions(), load_uncommon_definitions()]
    sort_by = ['Word', 'Reading', 'Index']
    df = pd.concat(dfs).sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded word definitions')
    return df


@cache
def load_common_definitions():
    logger.info('loading common word definitions ...')
    filename = 'word-definitions-common.csv'
    dtypes = {'SourceTypes': 'str', 'SourceWaseigo': 'str'}
    sort_by = ['Word', 'Reading', 'Index']
    df = data.load_csv(filename, dtypes=dtypes) \
        .sort_values(sort_by) \
        .reset_index(drop=True)
    logger.info('loaded common word definitions')
    return df


@cache
def load_uncommon_definitions():
    logger.info('loading uncommon word definitions ...')
    filename = 'word-definitions-uncommon.csv'
    dtypes = {'SourceTypes': 'str', 'SourceWaseigo': 'str'}
    sort_by = ['Word', 'Reading', 'Index']
    df = data.load_csv(filename, dtypes=dtypes) \
        .sort_values(sort_by) \
        .reset_index(drop=True)
    logger.info('loaded uncommon word definitions')
    return df


@cache
def count_components():
    logger.info('counting word components ...')
    counts = {}
    for composition in load_compositions().values():
        for component in composition:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted word components')
    return counts


@cache
def load_compositions():
    logger.info('loading word compositions')
    classify = component_classifier()
    compositions = {
        row['Word']: [
            (component, classify(component) or 'word-component')
            for component in row['Composition']
        ]
        for row in data.load_json('word-compositions.json')
    }
    logger.info('loaded word compositions')
    return compositions


@cache
def count_progression_components():
    logger.info('counting word progression components ...')
    counts = {}
    for progression in load_progressions().values():
        for component in progression:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted word progression components')
    return counts


@cache
def load_progressions():
    logger.info('loading word progressions ...')
    progressions = {
        row['Word']: [tuple(c) for c in row['Progression']]
        for row in data.load_json('word-progressions.json')
    }
    logger.info('loaded word progressions')
    return progressions


def progression_builder(compositions, kanji_progressions=None):
    if not kanji_progressions:
        kanji_progressions = kanji.load_progressions()
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
            # check for recursive components
            components = compositions.get(component[0], [])
            if any(c == root_component for c in components):
                continue
            # get the component's progression
            components = build_progression(component)
            # add new components or move them earlier in the progression
            progression = [c for c in progression if c not in components]
            progression = [*components, *progression]
        return progression
    return build_progression


def component_classifier(words=None, readings=None):
    if not words:
        words = set(load()['Word']).union(load_sometimes_kana()['Reading'])
    if not readings:
        readings = set(load()['Reading'])
    def classify(text):
        component_type = None
        if text in words:
            component_type = 'word'
        elif text in readings:
            component_type = 'word-reading'
        return component_type
    return classify
