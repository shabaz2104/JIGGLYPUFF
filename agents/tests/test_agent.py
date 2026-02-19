from agents.core.agent_runner import run_agent

if __name__ == "__main__":
    test_cases = [
        "Order 2 Paracetamol",
        "Is Paracetamol available?",
        "Show my previous orders",
        "Update stock of Paracetamol to 50"
    ]

    for case in test_cases:
        print("INPUT:", case)
        result = run_agent(case)
        print("OUTPUT:", result)
        print("-" * 50)
