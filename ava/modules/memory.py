from ava.core.storage import Storage
from datetime import datetime

class Memory:
    def __init__(self, storage=None):
        self.storage = storage or Storage()

    def add_birthday(self, name, date):
        birthdays = self.storage.get_section('birthdays')
        birthdays[name] = date
        self.storage.update_section('birthdays', birthdays)

    def get_birthdays(self):
        return self.storage.get_section('birthdays')

    def add_reminder(self, text, time):
        reminders = self.storage.get_section('reminders')
        reminders.append({"text": text, "time": time})
        self.storage.update_section('reminders', reminders)

    def get_reminders(self):
        return self.storage.get_section('reminders')

    def add_task(self, description):
        tasks = self.storage.get_section('tasks')
        tasks.append({"description": description, "completed": False, "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")})
        self.storage.update_section('tasks', tasks)

    def get_tasks(self):
        return self.storage.get_section('tasks')

    def check_alerts(self):
        alerts = []
        today = datetime.now().strftime("%B %d") # e.g. "October 05"

        # Check birthdays
        birthdays = self.get_birthdays()
        for name, date in birthdays.items():
            if today.lower() in date.lower():
                alerts.append(f"🎉 Birthday Alert: It's {name}'s birthday today!")

        # Check pending tasks
        tasks = self.get_tasks()
        pending_tasks = [t for t in tasks if not t.get("completed")]
        if pending_tasks:
            alerts.append(f"📝 You have {len(pending_tasks)} pending tasks.")

        return alerts
