import json
import os
import atexit
from datetime import datetime

class MemoryManager:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.environ.get("AVA_DATA_DIR", "ava/data")
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.memory_file = os.path.join(self.data_dir, "memory.json")
        self.habit_buffer_count = 0
        self.habit_buffer_limit = 50
        self.load_memory()
        atexit.register(self.flush)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "birthdays": {},
                "reminders": [],
                "tasks": [],
                "preferences": {},
                "habits": {}
            }
            self.save_memory()

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_birthday(self, name, date):
        self.data["birthdays"][name] = date
        self.save_memory()

    def add_reminder(self, text, time):
        self.data["reminders"].append({"text": text, "time": time})
        self.save_memory()

    def add_task(self, text):
        self.data["tasks"].append({"text": text, "completed": False})
        self.save_memory()

    def set_preference(self, key, value):
        self.data["preferences"][key] = value
        self.save_memory()

    def get_birthdays(self):
        return self.data["birthdays"]

    def get_reminders(self):
        return self.data["reminders"]

    def get_tasks(self):
        return self.data["tasks"]

    def get_preference(self, key, default=None):
        return self.data["preferences"].get(key, default)

    def track_habit(self, command):
        if command not in self.data["habits"]:
            self.data["habits"][command] = 0
        self.data["habits"][command] += 1

        self.habit_buffer_count += 1
        if self.habit_buffer_count >= self.habit_buffer_limit:
            self.save_memory()
            self.habit_buffer_count = 0

    def flush(self):
        """Force save memory to disk."""
        try:
            self.save_memory()
            self.habit_buffer_count = 0
        except (FileNotFoundError, OSError):
            # Handle cases where directory might be missing (e.g. tests)
            pass

    def get_habits(self):
        return self.data["habits"]
