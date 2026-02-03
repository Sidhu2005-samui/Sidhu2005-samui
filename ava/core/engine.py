import re
from ava.core.storage import Storage
from ava.core.adaptation import AdaptationEngine
from ava.modules.memory import Memory
from ava.modules.phone import PhoneModule
from ava.modules.whatsapp import WhatsAppModule
from ava.modules.instagram import InstagramModule
from ava.modules.research import ResearchModule

class AvaEngine:
    def __init__(self, storage_path='ava/data/storage.json'):
        self.storage = Storage(storage_path)
        self.adaptation = AdaptationEngine(self.storage)
        self.memory = Memory(self.storage)
        self.phone = PhoneModule()
        self.whatsapp = WhatsAppModule()
        self.instagram = InstagramModule()
        self.researcher = ResearchModule()

    def get_alerts(self):
        return self.memory.check_alerts()

    def process_input(self, user_input):
        original_input = user_input.strip()
        lower_input = original_input.lower()
        prefs = self.adaptation.get_preferences()

        # Phone calls
        if any(cmd in lower_input for cmd in ["call ", "dial ", "phone "]):
            # Extract name - very simple extraction
            name_part = re.sub(r'^(call|dial|phone)\s+', '', lower_input)
            name = name_part.strip().title()
            self.adaptation.log_action("call", {"name": name})
            return self.phone.make_call(name)

        # Research
        research_keywords = ["research ", "who is ", "what is ", "tell me about "]
        if any(kw in lower_input for kw in research_keywords):
            topic = original_input
            for kw in research_keywords:
                if kw in lower_input:
                    start_idx = lower_input.find(kw) + len(kw)
                    topic = original_input[start_idx:].strip()
                    break

            self.adaptation.log_action("research", {"topic": topic})
            pref_len = prefs.get("preferred_summary_length", "short")
            return self.researcher.research(topic, preferred_length=pref_len)

        # Reminders/Birthdays/Tasks
        if any(kw in lower_input for kw in ["remind me to ", "add task ", "to do "]):
            task = original_input
            for kw in ["remind me to ", "add task ", "to do "]:
                if kw in lower_input:
                    start_idx = lower_input.find(kw) + len(kw)
                    task = original_input[start_idx:].strip()
                    break
            self.memory.add_task(task)
            self.adaptation.log_action("memory", {"action": "add_task", "task": task})
            return f"Okay, I've added '{task}' to your tasks."

        if "birthday" in lower_input and " is " in lower_input:
            match = re.search(r"birthday of (.*) is (.*)", original_input, re.IGNORECASE)
            if match:
                name = match.group(1).strip().title()
                date = match.group(2).strip()
                self.memory.add_birthday(name, date)
                self.adaptation.log_action("memory", {"action": "add_birthday", "name": name, "date": date})
                return f"Got it! I've remembered {name}'s birthday on {date}."

        # WhatsApp mock
        if "whatsapp" in lower_input:
            match = re.search(r"whatsapp (.*) say (.*)", original_input, re.IGNORECASE)
            if match:
                recipient = match.group(1).strip().title()
                message = match.group(2).strip()
                self.adaptation.log_action("whatsapp", {"recipient": recipient})
                return self.whatsapp.send_message(recipient, message)

            # Simulated auto-reply check
            if "check messages" in lower_input:
                return self.whatsapp.auto_reply("Hi Ava!", "Unknown Sender")

        # Instagram mock
        if "instagram" in lower_input:
            if "comment" in lower_input:
                self.adaptation.log_action("instagram", {"action": "auto_comment"})
                return self.instagram.auto_comment("latest_post", "friend")

        # Check for alerts explicitly
        if any(kw in lower_input for kw in ["alerts", "notifications", "reminders"]):
            alerts = self.get_alerts()
            if alerts:
                return "Here are your alerts:\n" + "\n".join(alerts)
            return "No new alerts for today!"

        return "I'm not sure how to handle that yet. I'm still learning! You can ask me to call someone, research a topic, or add reminders."
