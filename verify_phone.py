from ava.modules.phone import PhoneModule

def test_phone():
    phone = PhoneModule()

    # Test specific requirement: "call Sion" calls Sayan
    result = phone.make_call("Sion")
    assert "Sayan" in result
    print(f"Result for 'Sion': {result}")

    # Test unknown name
    result = phone.make_call("John")
    assert "John" in result
    print(f"Result for 'John': {result}")

    print("Phone verification successful.")

if __name__ == "__main__":
    test_phone()
