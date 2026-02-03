import json
import os

class Storage:
    def __init__(self, filepath='ava/data/storage.json'):
        self.filepath = filepath
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({
                    "reminders": [],
                    "birthdays": {},
                    "tasks": [],
                    "preferences": {},
                    "history": []
                }, f)

    def load_data(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_section(self, section):
        data = self.load_data()
        return data.get(section)

    def update_section(self, section, new_value):
        data = self.load_data()
        data[section] = new_value
        self.save_data(data)
