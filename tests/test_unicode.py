import unittest
from streamstats.parsers import validator
from streamstats.models import Event

class TestUnicode(unittest.TestCase):

    def test_cyrillic_and_emoji_processing(self):
        """Проверка поддержки Unicode в полях лога (русские буквы)"""
        unicode_line = {
            "timestamp": "2026-10-18T12:00:00",
            "level": "WARNING",
            "source": "модуль_авторизации",
            "message": "Внимание: подозрительный вход! ⚠️"
        }
        event = validator(unicode_line)
        self.assertIsInstance(event, Event)
        self.assertEqual(event.source, "модуль_авторизации")
        self.assertEqual(event.message, "Внимание: подозрительный вход! ⚠️")

if __name__ == '__main__':
    unittest.main()
