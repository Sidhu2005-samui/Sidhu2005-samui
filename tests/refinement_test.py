import pytest
import os
from ava.core.engine import AvaEngine

@pytest.fixture
def engine():
    storage_path = 'ava/data/refinement_test_storage.json'
    if os.path.exists(storage_path):
        os.remove(storage_path)
    return AvaEngine(storage_path)

def test_adaptation_influence(engine):
    # Log research multiple times to trigger 'detailed' preference
    for _ in range(6):
        engine.process_input("research AI")

    # Now check if the next research is detailed
    res = engine.process_input("research Robotics")
    assert "Detailed Summary of Robotics" in res
    print(f"Refined Research Result: {res}")

def test_alerts(engine):
    # Add a task
    engine.process_input("remind me to Buy eggs")

    # Check alerts
    res = engine.process_input("show me alerts")
    assert "You have 1 pending tasks" in res
    print(f"Alerts Result: {res}")

if __name__ == "__main__":
    pytest.main([__file__])
