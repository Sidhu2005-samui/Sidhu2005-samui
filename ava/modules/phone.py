class PhoneModule:
    def __init__(self):
        # Example name mapping as requested: "call Sion" calls Sayan
        self.contacts = {
            "sion": "Sayan",
            "mom": "Mother",
            "boss": "The Big Chief"
        }

    def make_call(self, name):
        name_lower = name.lower()
        target = self.contacts.get(name_lower, name)
        return f"Calling {target}..."

    def add_contact(self, alias, actual_name):
        self.contacts[alias.lower()] = actual_name
