import logging
from functools import cache
from . import data, words


logger = logging.getLogger(__name__)


@cache
def load():
    logger.warning('progja.entities.load() is deprecated. Use '
        'progja.words.load_entities() instead.')
    return words.load_entities()
