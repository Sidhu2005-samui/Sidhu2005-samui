import sys
from ava.core.engine import AvaEngine

def main():
    ava = AvaEngine()
    print("Ava: Hello! I'm Ava, your super capable personal AI assistant.")
    print("Ava: How can I help you today? (Type 'exit' or 'quit' to stop)")

    # If arguments are provided, process them and exit (for non-interactive use/testing)
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"User: {query}")
        response = ava.process_input(query)
        print(f"Ava: {response}")
        return

    # Interactive loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Ava: Goodbye! Have a great day.")
                break

            response = ava.process_input(user_input)
            print(f"Ava: {response}")
        except KeyboardInterrupt:
            print("\nAva: Goodbye!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
