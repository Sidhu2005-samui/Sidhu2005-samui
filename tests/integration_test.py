import pytest
import os
import json
from ava.core.engine import AvaEngine

@pytest.fixture
def engine():
    storage_path = 'ava/data/integration_test_storage.json'
    if os.path.exists(storage_path):
        os.remove(storage_path)
    return AvaEngine(storage_path)

def test_full_flow(engine):
    # 1. Test Call with alias
    res = engine.process_input("call Sion")
    assert "Calling Sayan..." in res

    # 2. Test Research
    res = engine.process_input("research Space Exploration")
    assert "Summary of Space Exploration" in res

    # 3. Test Memory and Alert (Task)
    res = engine.process_input("remind me to Plan a surprise party")
    assert "Plan a surprise party" in res

    # 4. Test Birthday
    res = engine.process_input("birthday of Alice is January 1st")
    assert "Alice" in res

    # 5. Test WhatsApp
    res = engine.process_input("whatsapp Sion say See you tomorrow")
    assert "Sion" in res and "See you tomorrow" in res

    # 6. Test Instagram
    res = engine.process_input("comment on instagram")
    assert "Auto-commenting" in res

    # 7. Test Adaptation
    # Call Sion again to see if it logs correctly
    engine.process_input("call Sion")
    prefs = engine.adaptation.get_preferences()
    assert prefs["frequent_contacts"]["Sion"] == 2

if __name__ == "__main__":
    # Allow running this script directly as well
    pytest.main([__file__])
