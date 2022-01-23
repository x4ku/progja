import urllib.parse
import pandas as pd
from . import kanji, words, sentences


radical_id_pattern = 'progja:radical:{Kanji}'
kanji_id_pattern = 'progja:kanji:{Kanji}'
word_id_pattern = 'progja:word:{ID}'
sentence_id_pattern = 'progja:sentence:{Sentence}'


def create_cards(component, style=None):
    component_text, component_type = component
    if component_type == 'radical':
        return create_radical_cards(component, style)
    if component_type == 'kanji':
        return create_kanji_cards(component, style)
    if component_type == 'word':
        return create_word_cards(component, style)
    if component_type == 'sentence':
        return create_sentence_cards(component, style)
    return []


def create_radical_cards(component, style=None):
    component_text, component_type = component
    cards = []
    for radical in kanji.find(component_text):
        if pd.isna(radical['Meaning']):
            continue
        cards.append(create_radical_card(radical, style))
    return cards


def create_radical_card(radical, style=None, id_pattern=radical_id_pattern):
    return create_card(
        card_id=id_pattern.format(**radical),
        front=[
            *create_question_subject(
                'What is the meaning of the following radical?',
                create_jisho_link(radical['Kanji'], 'radical'),
                subject_classes=['text-japanese']
            ),
            *create_div(create_kanji_notes(radical), ['notes'])
        ],
        back=[
            *create_back_section('Meaning', radical['Meaning'], ['meaning']),
            *create_composition_section(
                '(none)' if pd.isna(radical['IDS'])
                else ''.join(create_span(radical['IDS'], ['text-japanese']))
            ),
            *create_progression_section(radical['Progression'])
        ],
        tags=create_radical_tags(radical),
        front_classes=['front-radical'],
        back_classes=['back-radical'],
        style=style
    )


def create_radical_tags(radical):
    return create_kanji_tags(radical)


def create_kanji_cards(component, style=None):
    component_text, component_type = component
    cards = []
    for kanji_ in kanji.find(component_text):
        if pd.isna(kanji_['Meaning']):
            continue
        cards.append(create_kanji_card(kanji_, style))
    return cards


def create_kanji_card(kanji, style=None, id_pattern=kanji_id_pattern):
    return create_card(
        card_id=id_pattern.format(**kanji),
        front=[
            *create_question_subject(
                'What is the meaning of the following kanji?',
                create_jisho_link(kanji['Kanji'], 'kanji'),
                subject_classes=['text-japanese']
            ),
            *create_div(create_kanji_notes(kanji), ['notes'])
        ],
        back=[
            *create_back_section('Meaning', kanji['Meaning'], ['meaning']),
            *create_composition_section(
                '(none)' if pd.isna(kanji['IDS'])
                else ''.join(create_span(kanji['IDS'], ['text-japanese']))
            ),
            *create_progression_section(kanji['Progression'])
        ],
        tags=create_kanji_tags(kanji),
        front_classes=['front-kanji'],
        back_classes=['back-kanji'],
        style=style
    )


def create_kanji_notes(kanji):
    notes = []
    if kanji['IsJouyou']:
        notes.append('Grade {} Jōyō kanji'.format(kanji['Grade']))
    if kanji['IsJinmeiyou']:
        notes.append('Grade {} Jinmeiyō kanji'.format(kanji['Grade']))
    if not pd.isna(kanji['JLPT']):
        notes.append('JLPT N{}'.format(kanji['JLPT']))
    return '({})'.format(', '.join(notes)) if notes else ''


def create_kanji_tags(kanji):
    kanji_tag = 'progja::kanji'
    tags = {kanji_tag}
    if kanji['IsRadical']:
        tags.add('{}::radical'.format(kanji_tag))
    if kanji['IsJouyou']:
        tags.add('{}::jouyou'.format(kanji_tag))
    if kanji['IsJinmeiyou']:
        tags.add('{}::jinmeiyou'.format(kanji_tag))
    if not pd.isna(kanji['Grade']):
        padded = '00{}'.format(kanji['Grade'])[-2:]
        tags.add('{}::grade::{}'.format(kanji_tag, padded))
    if not pd.isna(kanji['JLPT']):
        tags.add('{}::jlpt'.format(kanji_tag))
        tags.add('{}::jlpt::n{}'.format(kanji_tag, kanji['JLPT']))
    strokes = kanji['Strokes'] if not pd.isna(kanji['Strokes']) else 0
    padded = '00{}'.format(strokes)[-2:]
    tags.add('{}::strokes::{}'.format(kanji_tag, padded))
    return sorted(list(tags))


def create_word_cards(component, style=None):
    component_text, component_type = component
    found = words.find_common_or_any(component_text)
    cards = []
    for word in found:
        cards.append(create_word_card(word, style))
    return cards


def create_word_card(word, style=None, id_pattern=word_id_pattern):
    return create_card(
        card_id=id_pattern.format(**word),
        front=[
            *create_question_subject(
                'What is the definition of the following word?',
                create_jisho_link(word['Word'], 'word'),
                subject_classes=['text-japanese']
            ),
            *create_div(create_word_notes(word), ['notes'])
        ],
        back=[
            *create_back_section(
                'Reading',
                word['Reading'],
                ['reading'],
                contents_classes=['text-japanese']
            ),
            *create_back_section(
                'Definition',
                create_word_definition_list(word['Definitions']),
                ['definition']
            ),
            *create_progression_section(word['Progression'])
        ],
        tags=create_word_tags(word),
        front_classes=['front-word'],
        back_classes=['back-word'],
        style=style
    )


def create_word_notes(word):
    notes = []
    if word['IsCommon']:
        notes.append('Common word')
    reading_html = ''.join(create_span(word['Reading'], ['text-japanese']))
    if word['IsUsuallyKana']:
        notes.append('Usually written {}'.format(reading_html))
    elif word['IsSometimesKana']:
        notes.append('Sometimes written {}'.format(reading_html))
    return '({})'.format(', '.join(notes)) if notes else ''


def create_word_tags(word):
    word_tag = 'progja::word'
    tags = {word_tag}
    if word['IsCommon']:
        tags.add('{}::common'.format(word_tag))
    priority_tag = '{}::priority'.format(word_tag)
    if word['PriorityNF'] > 0:
        tags.add(priority_tag)
        padded = '00{}'.format(word['PriorityNF'])[-2:]
        tags.add('{}::nf::{}'.format(priority_tag, padded))
    if word['PriorityIchi'] > 0:
        tags.add(priority_tag)
        tags.add('{}::ichi::{}'.format(priority_tag, word['PriorityIchi']))
    if word['PriorityNews'] > 0:
        tags.add(priority_tag)
        tags.add('{}::news::{}'.format(priority_tag, word['PriorityNews']))
    if word['PrioritySpec'] > 0:
        tags.add(priority_tag)
        tags.add('{}::spec::{}'.format(priority_tag, word['PrioritySpec']))
    if word['PriorityGai'] > 0:
        tags.add(priority_tag)
        tags.add('{}::gai::{}'.format(priority_tag, word['PriorityGai']))
    if word['IsUsuallyKana']:
        tags.add('{}::usually_kana'.format(word_tag))
    if word['IsSometimesKana']:
        tags.add('{}::sometimes_kana'.format(word_tag))
    return sorted(list(tags))


def create_word_definition_list(definitions):
    entity_map = words.load_entities()
    items = []
    for definition in definitions:
        pos = '; '.join([
            entity_map.get(entity[1:-1], entity)
            for entity in definition['PartOfSpeech'].split(' ')
        ])
        items.append([
            *create_span(pos, ['part-of-speech']),
            *create_span(definition['Glosses'], ['glosses']),
        ])
    return create_ordered_list(items)


def create_sentence_cards(component, style=None):
    component_text, component_type = component
    cards = []
    for sentence in sentences.find(component_text):
        cards.append(create_sentence_card(sentence, style))
    return cards


def create_sentence_card(sentence, style=None, id_pattern=sentence_id_pattern):
    return create_card(
        card_id=id_pattern.format(**sentence),
        front=create_question_subject(
            'What is the translation of the following sentence?',
            sentence['Sentence'],
            subject_classes=['text-japanese']
        ),
        back=[
            *create_back_section(
                'Reading',
                sentence['Reading'],
                ['reading'],
                contents_classes=['text-japanese']
            ),
            *create_back_section(
                'Translations',
                create_unordered_list([
                    translation['Translation']
                    for translation in sentence['Translations']
                ]),
                ['translations']
            ),
            *create_progression_section(sentence['Progression'])
        ],
        tags=create_sentence_tags(sentence),
        front_classes=['front-sentence'],
        back_classes=['back-sentence'],
        style=style
    )


def create_sentence_tags(sentence):
    sentence_tag = 'progja::sentence'
    tags = {sentence_tag}
    return sorted(list(tags))


def create_card(
        card_id, front, back, tags, front_classes=None, back_classes=None,
        style=None):
    return {
        'ID': card_id,
        'Front': create_front(front, front_classes, style),
        'Back': create_back(back, back_classes, style),
        'Tags': ' '.join(tags)
    }


def create_front(contents, front_classes=None, style=None):
    front_classes = ['front', *(front_classes or [])]
    return ''.join([
        *(create_embedded_style_el(style) if style else []),
        *create_div(contents, front_classes)
    ])


def create_back(contents, back_classes=None, style=None):
    back_classes = ['back', *(back_classes or [])]
    return ''.join([
        *(create_embedded_style_el(style) if style else []),
        *create_div(contents, back_classes)
    ])


def create_question_subject(
        question, subject, question_classes=None, subject_classes=None):
    question = question if type(question) == list else [question]
    subject = subject if type(subject) == list else [subject]
    question_classes = ['question', *(question_classes or [])]
    subject_classes = ['subject', *(subject_classes or [])]
    return [
        *create_div(question, question_classes),
        *create_div(subject, subject_classes)
    ]


def create_composition_section(composition):
    return create_back_section(
        label='Composition',
        contents=composition,
        section_classes=['composition']
    )


def create_progression_section(progression):
    return create_back_section(
        label='Progression',
        contents=create_progression_list(progression),
        section_classes=['progression']
    )


def create_progression_list(progression):
    return create_ordered_list([
        [
            *create_span(
                create_jisho_link(component_text, component_type),
                ['component-text', 'text-japanese']
            ),
            ' (',
            *create_span(component_type, ['component-type']),
            ')'
        ]
        for component_text, component_type in progression
    ])


def create_back_section(
        label, contents, section_classes=None, label_classes=None,
        contents_classes=None):
    section_classes = ['section', *(section_classes or [])]
    label_classes = ['label', *(label_classes or [])]
    contents_classes = ['contents', *(contents_classes or [])]
    return create_div(
        contents=[
            *create_div('{}:'.format(label), label_classes),
            *create_div(contents, contents_classes)
        ],
        classes=section_classes
    )


def create_jisho_link(component_text, component_type):
    search_url = 'https://jisho.org/search'
    query = component_text
    if component_type in ('radical', 'kanji'):
        query = '{} #kanji'.format(component_text[0])
    href = '{}/{}'.format(search_url, urllib.parse.quote(query))
    return create_anchor(component_text, href)


def create_anchor(content, href, attributes=None):
    attributes = (attributes or {}) | {'href': href}
    return _create_el('a', content, attributes)


def create_embedded_style_el(style):
    return create_el('style', ' '.join([line.strip() for line in style]))


def create_div(contents, classes=None):
    return create_el('div', contents, classes)


def create_span(contents, classes=None):
    return create_el('span', contents, classes)


def create_ordered_list(items, list_classes=None, item_classes=None):
    return create_list(items, list_classes, item_classes, True)


def create_unordered_list(items, list_classes=None, item_classes=None):
    return create_list(items, list_classes, item_classes, False)


def create_list(items, list_classes=None, item_classes=None, ordered=True):
    return create_el(
        'ol' if ordered else 'ul',
        create_list_items(items, item_classes),
        list_classes
    )


def create_list_items(items, classes=None):
    return [''.join(create_list_item(item, classes)) for item in items]


def create_list_item(contents, classes=None):
    return create_el('li', contents, classes)


def create_el(el, contents, classes=None):
    classes = ' '.join(classes or [])
    return _create_el(el, contents, attributes={'class': classes})


def _create_el(el, contents, attributes=None):
    contents = contents if type(contents) == list else [contents]
    attributes_str = ' '.join([
        '{}="{}"'.format(key, value)
        for key, value in (attributes or {}).items()
    ])
    return [
        '<{} {}>'.format(el, attributes_str) if attributes
        else '<{}>'.format(el),
        *contents,
        '</{}>'.format(el)
    ]
