from ava.modules.memory import Memory
from ava.core.storage import Storage
import os

def test_memory():
    storage = Storage('ava/data/test_memory.json')
    memory = Memory(storage)

    memory.add_birthday("Alice", "1990-01-01")
    memory.add_task("Buy milk")
    memory.add_reminder("Meeting", "14:00")

    assert memory.get_birthdays()["Alice"] == "1990-01-01"
    assert memory.get_tasks()[0]["description"] == "Buy milk"
    assert memory.get_reminders()[0]["text"] == "Meeting"

    print("Memory verification successful.")

if __name__ == "__main__":
    test_memory()
