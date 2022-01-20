import logging
from functools import cache
from . import data


logger = logging.getLogger(__name__)

levels = (1, 2, 3, 4, 5)


@cache
def load_levels():
    return {level: load_level(level) for level in levels}


@cache
def load_level(level):
    filename = 'path-level-{}.csv'.format(level)
    if not data.exists('paths', filename):
        raise ValueError('Invalid path level')
    logger.info('loading level {} path ...'.format(level))
    df = data.read_csv('paths', filename) \
        .sort_values(['Order']) \
        .reset_index(drop=True)
    logger.info('loaded level {} path'.format(level))
    return df
