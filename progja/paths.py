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
    if not data.exists(filename):
        raise ValueError('Invalid path level')
    logger.info('loading level {} path ...'.format(level))
    sort_by = ['Order']
    df = data.load_csv(filename).sort_values(sort_by).reset_index(drop=True)
    logger.info('loaded level {} path'.format(level))
    return df
