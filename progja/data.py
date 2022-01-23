import json
import logging
import os
import pandas as pd


logger = logging.getLogger(__name__)

package_dir = os.path.realpath(os.path.dirname(__file__))
data_dir = os.path.join(package_dir, 'data')


def text_reader(build_path):
    def read(*path):
        with open(path(*path)) as file:
            lines = list(file)
        return lines
    return read


def csv_reader(build_path):
    def read(*path, dtypes=None):
        return pd.read_csv(build_path(*path), dtype=dtypes)
    return read


def jsonl_writer(build_path):
    def write(data, *path, **kwargs):
        if type(data) is not list:
            raise ValueError('data must be a list')
        indent = max(1, kwargs.pop('indent', 2))
        kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
        with open(build_path(*path), 'w') as file:
            file.write('[\n')
            for i, row in enumerate(data):
                file.write(''.join([
                    ' ' * indent,
                    json.dumps(row, **kwargs),
                    ',' if i < len(data) - 1 else '',
                    '\n'
                ]))
            file.write(']\n')
    return write


def json_reader(build_path):
    def read(*path, **kwargs):
        with open(build_path(*path)) as file:
            data = json.load(file, **kwargs)
        return data
    return read


def path_builder(root_path):
    def build(*path):
        return os.path.join(root_path, *path)
    return build


path = path_builder(data_dir)
def exists(*p): os.path.exists(path(*p))
read_text = text_reader(path)  # noqa: E305
read_csv = csv_reader(path)
write_jsonl = jsonl_writer(path)
read_json = json_reader(path)


def load_text(*args, **kwargs):
    logger.warning(
        'progja.data.load_text() is deprecated. Use progja.data.read_text() '
        'instead.')
    return read_text(*args, **kwargs)


def load_csv(*args, **kwargs):
    logger.warning(
        'progja.data.load_csv() is deprecated. Use progja.data.read_csv() '
        'instead.')
    return read_csv(*args, **kwargs)


def save_jsonl(*args, **kwargs):
    logger.warning(
        'progja.data.save_jsonl() is deprecated. Use progja.data.write_jsonl() '
        'instead.')
    return write_jsonl(*args, **kwargs)


def load_json(*args, **kwargs):
    logger.warning(
        'progja.data.load_json() is deprecated. Use progja.data.read_json() '
        'instead.')
    return read_json(*args, **kwargs)
