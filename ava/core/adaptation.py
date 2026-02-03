from ava.core.storage import Storage

class AdaptationEngine:
    def __init__(self, storage=None):
        self.storage = storage or Storage()

    def log_action(self, action_type, details):
        history = self.storage.get_section('history')
        history.append({"type": action_type, "details": details})
        self.storage.update_section('history', history)
        self._adapt_preferences(action_type, details)

    def _adapt_preferences(self, action_type, details):
        prefs = self.storage.get_section('preferences')

        # Simple adaptation: if user often calls someone, mark them as frequent
        if action_type == "call":
            name = details.get("name")
            frequent_contacts = prefs.get("frequent_contacts", {})
            frequent_contacts[name] = frequent_contacts.get(name, 0) + 1
            prefs["frequent_contacts"] = frequent_contacts

        # If user researches a lot, maybe they prefer detailed summaries?
        if action_type == "research":
            research_count = prefs.get("research_count", 0) + 1
            prefs["research_count"] = research_count
            if research_count > 5:
                prefs["preferred_summary_length"] = "detailed"

        self.storage.update_section('preferences', prefs)

    def get_preferences(self):
        return self.storage.get_section('preferences')
