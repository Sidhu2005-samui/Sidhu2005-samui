class WhatsAppModule:
    def __init__(self):
        self.auto_reply_enabled = True
        self.default_reply = "Hey! Ava here. I'm currently busy, but I'll get back to you soon."

    def set_auto_reply(self, enabled, message=None):
        self.auto_reply_enabled = enabled
        if message:
            self.default_reply = message

    def handle_incoming_message(self, contact, message):
        if self.auto_reply_enabled:
            return f"Auto-replying to {contact}: '{self.default_reply}'"
        return f"Message from {contact} received, but auto-reply is disabled."

    def send_message(self, contact, message):
        return f"Sending WhatsApp message to {contact}: {message}"
