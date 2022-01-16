import logging
from . import data, words


logger = logging.getLogger(__name__)


def load():
    logger.warning('progja.entities.load() is deprecated. Use '
        'progja.words.load_entities() instead.')
    return words.load_entities()
