import unittest
import os
import shutil
import asyncio
from ava.core.engine import AvaEngine

class TestAva(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = "tests/test_ava_data"
        os.environ["AVA_DATA_DIR"] = cls.test_dir

    def setUp(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        self.ava = AvaEngine()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_call_sion(self):
        response = asyncio.run(self.ava.process_input("Call Sion"))
        self.assertEqual(response, "Calling Sayan...")

    def test_research_ai(self):
        response = asyncio.run(self.ava.process_input("Research AI"))
        self.assertIn("intelligence", response.lower())

    def test_whatsapp_message(self):
        response = asyncio.run(self.ava.process_input("WhatsApp John Hello there"))
        self.assertEqual(response, "Sending WhatsApp message to John: Hello there")

    def test_whatsapp_auto_reply(self):
        # Testing via engine simulation
        response = asyncio.run(self.ava.process_input("Incoming message from Alice"))
        self.assertIn("Auto-replying to Alice", response)

    def test_instagram_comment(self):
        response = asyncio.run(self.ava.process_input("Comment on https://instagram.com/p/123"))
        self.assertIn("Auto-commenting on https://instagram.com/p/123", response)

    def test_reminder(self):
        response = asyncio.run(self.ava.process_input("Remind me to buy groceries at 5pm"))
        self.assertIn("buy groceries", response)
        self.assertIn("5pm", response)

    def test_birthday(self):
        response = asyncio.run(self.ava.process_input("Mom's birthday is on January 1st"))
        self.assertIn("Mom", response)
        self.assertIn("January 1st", response)

    def test_habit_adaptation(self):
        asyncio.run(self.ava.process_input("Call Sion"))
        asyncio.run(self.ava.process_input("Call Alice"))
        asyncio.run(self.ava.process_input("Call Bob"))
        summary = self.ava.get_summary()
        self.assertIn("call", summary)
        self.assertIn("Sion", summary) # Sion was the first one called in this session

if __name__ == "__main__":
    unittest.main()
