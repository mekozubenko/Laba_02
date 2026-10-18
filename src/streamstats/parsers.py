"""
Разделение файла на события.
"""
import csv
import json
from datetime import datetime
from streamstats.errors import InvalidEventError, InvalidTimestampError
from streamstats.models import Event

def read_csv(file_or_path):
    if isinstance(file_or_path, str):
        with open(file_or_path, newline='', encoding='utf-8') as csvfile:
            yield from csv.DictReader(csvfile)
    else:
        yield from csv.DictReader(file_or_path)


def read_json(file_or_path):
    if isinstance(file_or_path, str):
        with open(file_or_path, 'r', encoding='utf-8') as jsonfile:
            for line in jsonfile:
                if line.strip():
                    yield json.loads(line)
    else:
        for line in file_or_path:
            if line.strip():
                yield json.loads(line)


def validator(line):
    if not all(key in line for key in ('timestamp', 'level', 'source', 'message')):
        raise InvalidEventError('Несоответствие ключей.')
    try:
        datetime.fromisoformat(line['timestamp'])
    except:
        raise InvalidTimestampError('Неверная временная отметка.')
    if line['level'] not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
        raise InvalidEventError('Неверный уровень события.')
    if not line['source']:
        raise InvalidEventError('Пустая строка в источнике события.')
    return Event(line['timestamp'], line['level'], line['source'], line['message'])

def parser_csv(filename):
    stream = read_csv(filename)
    for event in stream:
        yield validator(event)

def parser_json(filename):
    stream = read_json(filename)
    for event in stream:
        yield validator(event)
