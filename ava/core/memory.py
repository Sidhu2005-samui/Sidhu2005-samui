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
        self.update_count = 0
        self.BUFFER_LIMIT = 50
        atexit.register(self.flush_memory)
        self.load_memory()

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
            self.flush_memory()

    def flush_memory(self):
        if not os.path.exists(self.data_dir):
            return
        with open(self.memory_file, "w") as f:
            json.dump(self.data, f, indent=4)
        self.update_count = 0

    def save_memory(self):
        self.update_count += 1
        if self.update_count >= self.BUFFER_LIMIT:
            self.flush_memory()

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
        self.save_memory()

    def get_habits(self):
        return self.data["habits"]
