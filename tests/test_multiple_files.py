import unittest
from streamstats.models import Event, Report
from streamstats.analysis import analyzer


class TestMultipleFiles(unittest.TestCase):

    def test_statistics_accumulation_from_multiple_sources(self):
        file1_events = [Event("2026-10-18T10:00:00", "INFO", "srv_1", "ok")]
        file2_events = [Event("2026-10-18T11:00:00", "ERROR", "srv_2", "fail")]

        all_events = file1_events + file2_events
        report = analyzer(all_events)

        self.assertEqual(report.events_count, 2)
        self.assertEqual(report.first_timestamp, "2026-10-18T10:00:00")
        self.assertEqual(report.last_timestamp, "2026-10-18T11:00:00")
        self.assertEqual(report.levels["INFO"], 1)
        self.assertEqual(report.levels["ERROR"], 1)


if __name__ == '__main__':
    unittest.main()
