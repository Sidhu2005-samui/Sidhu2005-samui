class PhoneModule:
    def __init__(self, contacts=None):
        # Default alias mapping as requested: "call Sion" calls Sayan
        self.contacts = contacts or {
            "Sion": "Sayan",
            "Mom": "Mother",
            "Dad": "Father"
        }

    def make_call(self, name):
        target = self.contacts.get(name, name)
        return f"Calling {target}..."

    def add_contact(self, alias, actual_name):
        self.contacts[alias] = actual_name
