import re
from ava.core.memory import MemoryManager
from ava.modules.phone import PhoneModule
from ava.modules.whatsapp import WhatsAppModule
from ava.modules.instagram import InstagramModule
from ava.modules.research import ResearchModule

class AvaEngine:
    def __init__(self):
        self.memory = MemoryManager()
        self.phone = PhoneModule()
        self.whatsapp = WhatsAppModule()
        self.instagram = InstagramModule()
        self.research = ResearchModule()

    def process_input(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return "How can I help you today?"

        # Track habits more intelligently
        self.track_habit_context(user_input)

        # 1. Phone Calls
        if re.search(r'\bcall\b', user_input, re.I):
            match = re.search(r'call\s+([\w\s]+)', user_input, re.I)
            if match:
                name = match.group(1).strip()
                return self.phone.make_call(name)
            return "Who should I call?"

        # 2. Research
        if re.search(r'\bresearch\b|\bwhat is\b|\bsearch for\b|\btell me about\b', user_input, re.I):
            query = re.sub(r'research|what is|search for|tell me about', '', user_input, flags=re.I).strip()
            if query:
                result = self.research.search(query)
                return self.research.summarize(result)
            return "What should I research for you?"

        # 3. Reminders / Birthdays
        if re.search(r'\bremind me\b|\balert\b', user_input, re.I):
            match = re.search(r'remind me (?:to|of)\s+(.+?)(?:\s+(?:at|on)\s+(.+))?$', user_input, re.I)
            if match:
                task = match.group(1).strip()
                time = match.group(2).strip() if match.group(2) else "later"
                self.memory.add_reminder(task, time)
                return f"Absolutely! I've set a reminder to {task} for {time}."
            return "What would you like me to remind you about?"

        if re.search(r'\bbirthday\b', user_input, re.I):
            match = re.search(r'([\w\s]+)\'s birthday is (?:on\s+)?(.+)', user_input, re.I)
            if match:
                name = match.group(1).strip()
                date = match.group(2).strip()
                self.memory.add_birthday(name, date)
                return f"Got it! I've noted that {name}'s birthday is on {date}. I'll make sure to alert you!"

        # 4. WhatsApp
        if re.search(r'\bwhatsapp\b|\bmessage\b', user_input, re.I):
            # Check for simulation of incoming message
            if "incoming" in user_input.lower():
                match = re.search(r'incoming\s+message\s+from\s+(\w+)', user_input, re.I)
                if match:
                    contact = match.group(1)
                    return self.whatsapp.handle_incoming_message(contact, "Hello")

            match = re.search(r'(?:whatsapp|message)\s+(\w+)\s+(.+)', user_input, re.I)
            if match:
                contact = match.group(1)
                msg = match.group(2)
                return self.whatsapp.send_message(contact, msg)
            return "To whom should I send a message, and what should it say?"

        # 5. Instagram
        if re.search(r'\binstagram\b|\bcomment\b', user_input, re.I):
            match = re.search(r'(?:instagram|comment)\s+(?:on\s+)?(https?://\S+)', user_input, re.I)
            if match:
                url = match.group(1)
                return self.instagram.comment_on_post(url)
            return "Please provide a valid Instagram post URL for me to comment on."

        # 6. Preferences
        if re.search(r'\bset preference\b', user_input, re.I):
            match = re.search(r'set preference\s+(\w+)\s+to\s+(.+)', user_input, re.I)
            if match:
                key = match.group(1)
                val = match.group(2)
                self.memory.set_preference(key, val)
                return f"Understood. I've updated your preference for '{key}' to '{val}'."

        # 7. Status / Adaptation info
        if "status" in user_input.lower() or "how are you" in user_input.lower():
            return self.get_summary()

        return "I'm not quite sure how to do that yet, but I'm learning! You can ask me to make calls, research topics, set reminders, or manage your messages."

    def track_habit_context(self, user_input):
        words = user_input.lower().split()
        if not words: return

        verb = words[0]
        self.memory.track_habit(verb)

        # Adaptation: If user often calls someone, we could suggest it (simplified here)
        if verb == "call" and len(words) > 1:
            name = words[1]
            # Store frequent contacts
            fav_contacts = self.memory.get_preference("frequent_contacts", {})
            fav_contacts[name] = fav_contacts.get(name, 0) + 1
            self.memory.set_preference("frequent_contacts", fav_contacts)

    def get_summary(self):
        habits = self.memory.get_habits()
        most_used = max(habits, key=habits.get) if habits else "None"
        favs = self.memory.get_preference("frequent_contacts", {})
        top_contact = max(favs, key=favs.get) if favs else "None"

        return (f"I'm Ava, your assistant. I've noticed you frequently use the '{most_used}' command. "
                f"Your most contacted person seems to be {top_contact.capitalize()}. "
                "I'm ready for your next task!")
