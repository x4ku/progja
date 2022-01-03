import csv
import json
import logging
import os
import pandas as pd


logger = logging.getLogger(__name__)

package_dir = os.path.realpath(os.path.dirname(__file__))
data_dir = os.path.join(package_dir, 'data')


def load_text(*paths):
    with open(path(*paths)) as file:
        lines = list(file)
    return lines


def load_csv(*paths, dtypes=None):
    return pd.read_csv(path(*paths), dtype=dtypes)


def save_jsonl(data, *paths, **kwargs):
    if type(data) is not list:
        raise ValueError('data must be a list')
    indent = max(1, kwargs.pop('indent', 2))
    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
    with open(path(*paths), 'w') as file:
        file.write('[\n')
        for i, row in enumerate(data):
            file.write(''.join([
                ' ' * indent,
                json.dumps(row, **kwargs),
                ',' if i < len(data) - 1 else '',
                '\n'
            ]))
        file.write(']\n')


def load_json(*paths, **kwargs):
    with open(path(*paths)) as file:
        data = json.load(file, **kwargs)
    return data


def exists(*paths):
    return os.path.exists(path(*paths))


def path(*paths):
    return os.path.join(data_dir, *paths)
