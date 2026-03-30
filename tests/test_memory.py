import unittest
import os
import shutil
import json
import time
from ava.core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_data_memory"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir) # Ensure dir exists for environment variable to be valid?
        # Actually MemoryManager handles creation.
        os.environ["AVA_DATA_DIR"] = self.test_dir
        self.mm = MemoryManager()
        self.memory_file = os.path.join(self.test_dir, "memory.json")

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

    def test_buffering_behavior(self):
        # Initial state: file should contain empty habits (from load_memory -> flush_memory)
        with open(self.memory_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data.get("habits", {}), {})

        # 49 updates
        for i in range(49):
            self.mm.track_habit(f"habit_{i}")

        # Check file content: should still be empty (buffered)
        with open(self.memory_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data.get("habits", {}), {}, "File should not be updated yet")

        # 50th update
        self.mm.track_habit("habit_50")

        # Check file content: should be updated (flushed)
        with open(self.memory_file, "r") as f:
            data = json.load(f)
        self.assertIn("habit_50", data["habits"], "File should be updated after 50th update")
        self.assertEqual(len(data["habits"]), 50)

if __name__ == "__main__":
    unittest.main()
