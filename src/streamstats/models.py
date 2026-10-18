"""
Описание модели события.
"""
class Event:
    def __init__(self, timestamp, level, source, message):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message
    def __str__(self):
        return f'Отметка времени: {self.timestamp}\nУровень: {self.level}\nИсточник: {self.source}\nСообщение: {self.message}'


class Report:
    def __init__(self):
        self.events_count = 0
        self.levels = dict()
        self.sources = dict()
        self.critical_sources = dict()
        self.top_5_error_sources = []
        self.first_timestamp = None
        self.last_timestamp = None
        self.skipped_lines = 0
