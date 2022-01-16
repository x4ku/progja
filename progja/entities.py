import csv
import logging
from functools import cache
from . import data


logger = logging.getLogger(__name__)


@cache
def load():
    logger.info('loading entities ...')
    entities = {}
    with open(data.path('words', 'entities.csv')) as file:
        for row in list(csv.DictReader(file)):
            entities[row['Entity']] = row['Description']
    logger.info('loaded entities')
    return entities
