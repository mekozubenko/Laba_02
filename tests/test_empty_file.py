import unittest
from streamstats.analysis import analyzer


class TestEmptyFile(unittest.TestCase):

    def test_analyzer_with_no_events(self):
        """
        Проверяет, что пустой файл возвращает пустой отчет.
        """
        empty_generator = []
        report = analyzer(empty_generator)

        self.assertEqual(report.events_count, 0)
        self.assertIsNone(report.first_timestamp)
        self.assertIsNone(report.last_timestamp)
        self.assertEqual(len(report.levels), 0)
        self.assertEqual(len(report.sources), 0)


if __name__ == '__main__':
    unittest.main()
