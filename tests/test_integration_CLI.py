import unittest
import os
import json
import sys
from tempfile import TemporaryDirectory
from streamstats.__main__ import main


class TestIntegrationCLI(unittest.TestCase):

    def test_cli_execution_with_temp_dir(self):
        """
        Интеграционный тест: создание файлов на диске, запуск main() и проверка JSON-отчета
        """
        with TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.jsonl")
            output_report = os.path.join(tmpdir, "report.json")

            with open(input_file, "w", encoding="utf-8") as f:
                f.write(
                    '{"timestamp": "2026-10-18T12:00:00", "level": "INFO", "source": "cli_test", "message": "hello"}\n')

            old_argv = sys.argv
            sys.argv = [
                "streamstats", "analyze",
                input_file,
                "--format", "jsonl",
                "--output", output_report
            ]

            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            finally:
                sys.argv = old_argv

            self.assertTrue(os.path.exists(output_report))
            with open(output_report, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data['Общее число событий'], 1)
            self.assertEqual(data['Первая временная метка'], "2026-10-18T12:00:00")

if __name__ == '__main__':
    unittest.main()
