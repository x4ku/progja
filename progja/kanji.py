import logging
from functools import cache
from random import randint
from . import data


logger = logging.getLogger(__name__)

grades_jouyou_primary = (1, 2, 3, 4, 5, 6)
grades_jouyou_secondary = (8,)
grades_jouyou = (*grades_jouyou_primary, *grades_jouyou_secondary)
grades_jinmeiyou = (9, 10)
grades = (*grades_jouyou, *grades_jinmeiyou)
substitutions = {}


def random(jouyou=False, jinmeiyou=False):
    df = (
        load_jouyou() if jouyou
        else load_jinmeiyou() if jinmeiyou
        else load()
    )
    index = randint(0, len(df) - 1)
    return find(df.iloc[index]['Kanji'])


def find(character):
    df = load()
    compositions = load_compositions()
    progressions = load_progressions()
    df2 = df[df['Kanji'] == character]
    records = df2.to_dict('records')
    for record in records:
        record['Composition'] = compositions.get(record['Kanji'], [])
        record['Progression'] = progressions.get(record['Kanji'], [])
    return records


@cache
def load_radicals():
    logger.info('loading radicals ...')
    df = load()
    df = df[df['IsRadical']] \
        .sort_values(['Grade', 'Strokes', 'Kanji']) \
        .reset_index(drop=True)
    logger.info('loaded radicals')
    return df


@cache
def load_jouyou():
    logger.info('loading Jōyō kanji ...')
    df = load()
    df = df[df['IsJouyou']] \
        .sort_values(['Grade', 'Strokes', 'Kanji']) \
        .reset_index(drop=True)
    logger.info('loaded Jōyō kanji')
    return df


@cache
def load_jinmeiyou():
    logger.info('loading Jinmeiyō kanji ...')
    df = load()
    df = df[df['IsJinmeiyou']] \
        .sort_values(['Grade', 'Strokes', 'Kanji']) \
        .reset_index(drop=True)
    logger.info('loaded Jinmeiyō kanji')
    return df


@cache
def load():
    logger.info('loading kanji ...')
    dtypes = {
        'Grade': 'Int64',
        'JLPT': 'Int64',
        'Strokes': 'Int64'
    }
    df = data.read_csv('kanji', 'kanji.csv', dtypes=dtypes) \
        .sort_values(['Grade', 'Strokes', 'Kanji']) \
        .reset_index(drop=True)
    logger.info('loaded kanji')
    return df


@cache
def count_components():
    logger.info('counting kanji components ...')
    counts = {}
    for composition in load_compositions().values():
        for component in composition:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted kanji components')
    return counts


@cache
def load_compositions():
    logger.info('loading kanji compositions ...')
    df = load()
    kanji_set = set(df['Kanji'])
    classify = component_classifier()
    compositions = {}
    series = (df['Kanji'], df['Components'].fillna(''))
    for kanji, components in zip(*series):
        components = [
            substitutions.get(component, component)
            for component in filter(None, components.split(' '))
        ]
        composition = []
        for component in components:
            if component[0] not in kanji_set:
                continue
            composition.append((component, classify(component)))
        compositions[kanji] = composition
    logger.info('loaded kanji compositions')
    return compositions


@cache
def count_progression_components():
    logger.info('counting kanji progression components ...')
    counts = {}
    for progression in load_progressions().values():
        for component in progression:
            counts.setdefault(component, 0)
            counts[component] += 1
    counts = dict(sorted(counts.items(), key=lambda c: -1 * c[1]))
    logger.info('counted kanji progression components')
    return counts


@cache
def load_progressions():
    logger.info('loading kanji progressions ...')
    rows = data.read_json('kanji', 'kanji-progressions.json')
    progressions = {
        row['Kanji']: [tuple(c) for c in row['Progression']]
        for row in rows
    }
    logger.info('loaded kanji progressions')
    return progressions


def progression_builder(compositions):
    def build_progression(root_component):
        # if the root component is a variant, remember it for later
        variant = None
        if len(root_component[0]) > 1:
            variant = root_component
            # reassign the root component
            component_type = (
                'kanji' if root_component[1] == 'kanji-variant'
                else 'radical' if root_component[1] == 'radical-variant'
                else 'kanji-component'
            )
            root_component = (root_component[0][0], component_type)
        # start the progression with the root component
        progression = [root_component]
        # add progressions for each subcomponent
        composition = compositions.get(root_component[0], [])
        for component in composition[::-1]:
            # check for variant components
            if component[0][0] == root_component[0][0]:
                if len(component[0]) > 1:
                    if component not in progression:
                        progression.append(component)
                continue
            # check for recursive components
            components = compositions.get(component[0], [])
            if any(c in (root_component, variant) for c in components):
                continue
            # get the component's progression
            components = build_progression(component)
            # add new components or move them earlier in the progression
            progression = [c for c in progression if c not in components]
            progression = [*components, *progression]
        # if the root component was a variant, add it to the end
        if variant:
            if variant in progression:
                progression.remove(variant)
            progression.append(variant)
        return progression
    return build_progression


def component_classifier(kanji=None, radicals=None):
    if not kanji:
        kanji = set(load()['Kanji'])
    if not radicals:
        radicals = set(load_radicals()['Kanji'])

    def classify(text):
        component_type = None
        if len(text) > 1:
            if text[0] in kanji:
                component_type = 'kanji-variant'
            elif text[0] in radicals:
                component_type = 'radical-variant'
            else:
                component_type = 'unknown-variant'
        elif text in radicals:
            component_type = 'radical'
        elif text in kanji:
            component_type = 'kanji'
        return component_type
    return classify


substitutions = {
    # variants:
    '丷': '丶(丷)',
    '⺄': '乙(⺄)',
    '⺃': '乙(乚)',
    '乚': '乙(乚)',
    '乛': '乙(乛)',
    '龴': '乙(龴)',
    '亻': '人(亻)',
    '𠂉': '人(𠂉)',
    '𠆢': '人(𠆢)',
    '㇇': '今(㇇)',
    '⺆': '冂(⺆)',
    '⺇': '几(⺇)',
    '⺈': '刀(⺈)',
    '刂': '刀(刂)',
    '⺊': '卜(⺊)',
    '⺁': '厂(⺁)',
    '孑': '子(孑)',
    '⺌': '小(⺌)',
    '𭕄': '小(⺍)',
    '⺍': '小(⺍)',
    '⺎': '尢(⺎)',
    '巛': '川(巛)',
    '卄': '廿(卄)',
    '⺔': '彐(⺔)',
    '⺕': '彐(⺕)',
    '⺗': '心(⺗)',
    '㣺': '心(⺗)',
    '忄': '心(忄)',
    '戶': '戸(戶)',
    '户': '戸(户)',
    '扌': '手(扌)',
    '龵': '手(龵)',
    '⺙': '攴(⺙)',
    '齊': '斉(齊)',
    '⺜': '日(⺜)',
    '⺞': '歹(⺞)',
    '毌': '毋(毌)',
    '每': '毎(每)',
    '⺢': '水(⺢)',
    '氵': '水(氵)',
    '氺': '水(氺)',
    '冫': '氷(冫)',
    '⺣': '火(灬)',
    '灬': '火(灬)',
    '⺤': '爪(⺤)',
    '爫': '爪(爫)',
    '⺧': '牛(⺧)',
    '牜': '牛(牜)',
    '犭': '犬(犭)',
    '⺩': '玉(⺩)',
    '⺪': '疋(⺪)',
    '⺫': '目(⺫)',
    '⺭': '示(⺭)',
    '礻': '示(礻)',
    '⺮': '竹(⺮)',
    '⺯': '糸(⺯)',
    '⺰': '糸(⺰)',
    '糹': '糸(糹)',
    '⺱': '网(⺱)',
    '⺲': '网(⺲)',
    '⺳': '网(⺳)',
    '⺴': '网(⺴)',
    '⺶': '羊(⺶)',
    '⺷': '羊(⺷)',
    '⺸': '羊(⺸)',
    '𦍌': '羊(𦍌)',
    '⺹': '老(⺹)',
    '耂': '老(耂)',
    '⺻': '聿(⺻)',
    '肀': '聿(肀)',
    '𦘒': '聿(𦘒)',
    '⺼': '肉(⺼)',
    '⺾': '艸(⺾)',
    '⺿': '艸(⺿)',
    '⻀': '艸(⻀)',
    '䒑': '艸(䒑)',
    '艹': '艸(艹)',
    '⻂': '衣(⻂)',
    '衤': '衣(衤)',
    '⻃': '西(⻃)',
    '襾': '西(襾)',
    '覀': '西(覀)',
    '訁': '言(訁)',
    '豖': '豕(豖)',
    '𧾷': '足(𧾷)',
    '⻌': '辵(⻌)',
    '⻍': '辵(⻍)',
    '辶': '辵(⻍)',
    '⻎': '辵(⻎)',
    '⻏': '邑(⻏)',
    '釒': '金(釒)',
    '镸': '長(镸)',
    '⻔': '門(⻔)',
    '⻖': '阜(⻖)',
    '阝': '阜(阝)',
    '⻗': '雨(⻗)',
    '靑': '青(靑)',
    '⻛': '風(⻛)',
    '⻞': '食(⻞)',
    '⻟': '食(⻟)',
    '⻠': '食(⻠)',
    '飠': '食(飠)',
    '𩙿': '食(𩙿)',
    '⻢': '馬(⻢)',
    '⻥': '魚(⻥)',
    '⻦': '鳥(⻦)',
    '麥': '麦(麥)',
    '⻩': '黃(⻩)',
    '黃': '黄(黃)',
    '黒': '黑(黒)',
    '歯': '齒(歯)',
    '亀': '龜(亀)',
    '𤣩': '王(𤣩)',
    # miscellaneous:
    '⼹': '彐',
    '⽖': '爪',
    '⾆': '舌',
    '⻨': '麦',
}
