import unittest
import os
import json

from streamstats.models import Report, Event
from streamstats.errors import StreamStatsError
from streamstats.parsers import validator


class TestInvalidLinesSimple(unittest.TestCase):

    def test_mode_without_skip(self):
        """
        Тест режима по умолчанию (без пропуска ошибочных строк).
        """
        raw_lines = [
            {"timestamp": "2026-10-18T12:00:00", "level": "INFO", "source": "app", "message": "ok"},
            {"timestamp": "not-a-date", "level": "INFO", "source": "app", "message": "bad"}
        ]

        program_dropped = False

        try:
            for line in raw_lines:
                clean_event = validator(line)
        except StreamStatsError:
            program_dropped = True

        self.assertEqual(program_dropped, True)

    def test_mode_with_skip_invalid(self):
        """
        Тест режима с пропуском ошибок и выводом номера строки с ошибкой (skip-invalid)
        """
        raw_lines = [
            {"timestamp": "2026-10-18T12:00:00", "level": "INFO", "source": "app", "message": "ok1"},
            {"timestamp": "not-a-date", "level": "INFO", "source": "app", "message": "bad"},
            {"timestamp": "2026-10-18T13:00:00", "level": "DEBUG", "source": "app", "message": "ok2"}
        ]

        test_report = Report()

        for line in raw_lines:
            try:
                event = validator(line)
                test_report.events_count += 1
            except StreamStatsError:
                test_report.skipped_lines += 1

        self.assertEqual(test_report.events_count, 2)
        self.assertEqual(test_report.skipped_lines, 1)


if __name__ == '__main__':
    unittest.main()
