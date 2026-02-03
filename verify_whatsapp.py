from ava.modules.whatsapp import WhatsAppModule

def test_whatsapp():
    wa = WhatsAppModule()

    reply1 = wa.auto_reply("Hello there", "John")
    assert "Hi! I'm Ava" in reply1
    print(f"Reply to Hello: {reply1}")

    reply2 = wa.auto_reply("Can we meet?", "Alice")
    assert "busy right now" in reply2
    print(f"Reply to other: {reply2}")

    print("WhatsApp verification successful.")

if __name__ == "__main__":
    test_whatsapp()
