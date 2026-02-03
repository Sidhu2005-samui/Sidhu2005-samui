from ava.core.engine import AvaEngine
import os

def test_engine():
    engine = AvaEngine('ava/data/test_engine.json')

    # Test call
    res = engine.process_input("call Sion")
    assert "Sayan" in res
    print(f"Call Result: {res}")

    # Test research
    res = engine.process_input("research AI")
    assert "Summary of AI" in res
    print(f"Research Result: {res}")

    # Test memory
    res = engine.process_input("remind me to Buy groceries")
    assert "Buy groceries" in res
    print(f"Memory Result: {res}")

    # Test birthday
    res = engine.process_input("birthday of Bob is October 5th")
    assert "Bob" in res and "October 5th" in res
    print(f"Birthday Result: {res}")

    print("Engine verification successful.")

if __name__ == "__main__":
    test_engine()
