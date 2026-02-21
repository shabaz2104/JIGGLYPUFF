from agents.core.agent_runner import run_agent

if __name__ == "__main__":

    test_inputs = [
        # Order test
        "Order 2 Paracetamol",

        # Inventory test
        "Is Paracetamol available?",

        # History test
        "Show my previous orders",

        # Update stock test (delta-based)
        "Increase Paracetamol stock by 5",

        # Follow-up memory test
        "Order 1 more of that medicine",

        # Predictive intelligence test
        "Hi"
    ]

    for user_input in test_inputs:
        print("\nINPUT:", user_input)

        result = run_agent(user_input)

        print("OUTPUT:", result)
        print("-" * 60)