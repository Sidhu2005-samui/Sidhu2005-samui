from ava.core.storage import Storage
import os

def test_storage():
    storage = Storage('ava/data/test_storage.json')

    # Test section update
    storage.update_section('preferences', {'theme': 'dark'})

    # Test section retrieval
    prefs = storage.get_section('preferences')
    assert prefs == {'theme': 'dark'}

    # Verify file content
    data = storage.load_data()
    assert data['preferences'] == {'theme': 'dark'}
    print("Storage verification successful.")

if __name__ == "__main__":
    test_storage()
