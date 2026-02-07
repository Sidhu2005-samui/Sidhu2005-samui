import unittest
import os
import shutil
import json
from ava.core.memory import MemoryManager

class TestMemoryBuffering(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_data_memory_buffering"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.environ["AVA_DATA_DIR"] = self.test_dir
        self.mm = MemoryManager()
        # Override limit for testing
        self.mm.habit_buffer_limit = 5

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_buffering_logic(self):
        # Initial state
        self.mm.track_habit("test_cmd")
        # Should be 1 in memory
        self.assertEqual(self.mm.get_habits()["test_cmd"], 1)

        # Check disk - should be empty/default (or not contain "test_cmd" if save_memory wasn't called)
        # Note: save_memory is called in __init__ to create the file if it doesn't exist.
        # So the file exists, but "habits" should be empty.

        mm_disk = MemoryManager() # Reads from same dir
        self.assertNotIn("test_cmd", mm_disk.get_habits())

        # Track 3 more times (total 4) - limit is 5
        self.mm.track_habit("test_cmd")
        self.mm.track_habit("test_cmd")
        self.mm.track_habit("test_cmd")

        self.assertEqual(self.mm.get_habits()["test_cmd"], 4)

        mm_disk = MemoryManager()
        self.assertNotIn("test_cmd", mm_disk.get_habits())

        # Track 5th time - should trigger save
        self.mm.track_habit("test_cmd")
        self.assertEqual(self.mm.get_habits()["test_cmd"], 5)

        mm_disk = MemoryManager()
        self.assertIn("test_cmd", mm_disk.get_habits())
        self.assertEqual(mm_disk.get_habits()["test_cmd"], 5)

    def test_flush(self):
        self.mm.track_habit("flush_cmd")
        self.assertEqual(self.mm.get_habits()["flush_cmd"], 1)

        # Not saved yet
        mm_disk = MemoryManager()
        self.assertNotIn("flush_cmd", mm_disk.get_habits())

        # Flush
        self.mm.flush()

        # Saved now
        mm_disk = MemoryManager()
        self.assertIn("flush_cmd", mm_disk.get_habits())
        self.assertEqual(mm_disk.get_habits()["flush_cmd"], 1)

if __name__ == "__main__":
    unittest.main()
