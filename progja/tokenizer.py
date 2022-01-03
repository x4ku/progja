from sudachipy import Dictionary, SplitMode


tokenizer = Dictionary().create()


def decompose(value):
    composition = dict()
    for token_min in tokenize(value):
        # add components with maximum segmentation
        for token_max in token_min['Tokens']:
            composition[token_max['Lemma']] = None
        # add component with minimum segmentation
        composition[token_min['Lemma']] = None
    return list(composition.keys())


def tokenize(value, segmentation=1):
    split_mode = get_split_mode(segmentation)
    morphemes = tokenizer.tokenize(value, split_mode)
    return [
        {
            **morpheme_to_token(morpheme),
            'Tokens': [
                morpheme_to_token(morpheme2)
                for morpheme2 in morpheme.split(get_split_mode(3))
            ]
        }
        for morpheme in morphemes
    ]


def morpheme_to_token(morpheme):
    return {
        'Surface': morpheme.surface(),
        'Root': morpheme.dictionary_form(),
        'Lemma': morpheme.normalized_form(),
        'Reading': morpheme.reading_form(),
        'PartOfSpeech': ' '.join(morpheme.part_of_speech())
    }


def get_split_mode(segmentation=1):
    if segmentation not in (1, 2, 3):
        raise ValueError('segmentation must be between 1 (min) and 3 (max)')
    if segmentation == 3:
        return SplitMode.A
    if segmentation == 2:
        return SplitMode.B
    return SplitMode.C
