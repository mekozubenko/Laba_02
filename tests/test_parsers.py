import unittest
import io
from streamstats.parsers import read_csv, read_json


class TestUnitParsers(unittest.TestCase):

    def test_csv_parser(self):
        """
        Проверяет, что CSV парсер корректно разбирает строки по ключам
        """
        csv_content = "timestamp,level,source,message\n2026-10-18T12:00:00,INFO,srv,ok\n"
        file_mock = io.StringIO(csv_content)

        rows = list(read_csv(file_mock))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['level'], "INFO")
        self.assertEqual(rows[0]['source'], "srv")

    def test_json_parser(self):
        """
        Проверяет, что JSONL парсер корректно считывает JSON-строки
        """
        jsonl_content = '{"timestamp": "2026-10-18T12:00:00", "level": "DEBUG", "source": "srv", "message": "hi"}\n'
        file_mock = io.StringIO(jsonl_content)

        rows = list(read_json(file_mock))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['level'], "DEBUG")
        self.assertEqual(rows[0]['source'], "srv")


if __name__ == '__main__':
    unittest.main()
