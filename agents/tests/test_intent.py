from agents.core.intent_classifier import classify_intent

if __name__ == "__main__":
    test_cases = [
        "I want 2 Paracetamol",
        "Is Paracetamol available?",
        "Show my previous orders",
        "Update stock of Paracetamol to 50"
    ]

    for case in test_cases:
        intent = classify_intent(case)
        print(f"Input: {case}")
        print(f"Intent: {intent}")
        print("-" * 40)
