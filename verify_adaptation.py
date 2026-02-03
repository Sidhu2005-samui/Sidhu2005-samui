from ava.core.adaptation import AdaptationEngine
from ava.core.storage import Storage

def test_adaptation():
    storage = Storage('ava/data/test_adaptation.json')
    engine = AdaptationEngine(storage)

    # Log some calls
    engine.log_action("call", {"name": "Sion"})
    engine.log_action("call", {"name": "Sion"})

    prefs = engine.get_preferences()
    assert prefs["frequent_contacts"]["Sion"] == 2

    # Log research multiple times to trigger adaptation
    for _ in range(6):
        engine.log_action("research", {"topic": "AI"})

    prefs = engine.get_preferences()
    assert prefs["research_count"] >= 6
    assert prefs["preferred_summary_length"] == "detailed"

    print("Adaptation verification successful.")

if __name__ == "__main__":
    test_adaptation()
