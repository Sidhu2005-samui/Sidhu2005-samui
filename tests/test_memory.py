import unittest
import os
import shutil
import json
from ava.core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_data_memory"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.environ["AVA_DATA_DIR"] = self.test_dir
        self.mm = MemoryManager()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_birthday(self):
        self.mm.add_birthday("Alice", "1990-01-01")
        self.assertEqual(self.mm.get_birthdays()["Alice"], "1990-01-01")

    def test_add_reminder(self):
        self.mm.add_reminder("Buy milk", "2023-10-27 10:00")
        reminders = self.mm.get_reminders()
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0]["text"], "Buy milk")

    def test_add_task(self):
        self.mm.add_task("Clean room")
        tasks = self.mm.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Clean room")

    def test_preferences(self):
        self.mm.set_preference("theme", "dark")
        self.assertEqual(self.mm.get_preference("theme"), "dark")

    def test_habits(self):
        self.mm.track_habit("call")
        self.mm.track_habit("call")
        self.assertEqual(self.mm.get_habits()["call"], 2)

    def test_add_note(self):
        self.mm.add_note("Meeting notes: Discuss API keys")
        notes = self.mm.get_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Meeting notes: Discuss API keys")
        self.assertTrue("timestamp" in notes[0])

if __name__ == "__main__":
    unittest.main()
