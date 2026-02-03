import sys
from ava.core.engine import AvaEngine

def main():
    print("Ava: Hello! I'm Ava, your super capable personal assistant.")

    engine = AvaEngine()

    # Show initial alerts
    alerts = engine.get_alerts()
    if alerts:
        print("\n--- Daily Briefing ---")
        for alert in alerts:
            print(alert)
        print("----------------------\n")

    print("How can I help you today?")
    print("(Type 'exit' or 'quit' to leave, or 'alerts' to see notifications)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Ava: Goodbye!")
                break

            response = engine.process_input(user_input)
            print(f"Ava: {response}")

        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nAva: Goodbye!")
            break

if __name__ == "__main__":
    main()
