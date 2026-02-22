from agents.core.extractor import extract_structured_request

tests = [
    "Order 2 Paracetamol",
    "Is Paracetamol available?",
    "Show my previous orders",
    "Update stock of Paracetamol to 50"
]

for t in tests:
    result = extract_structured_request(t)
    print("Input:", t)
    print("Output:", result)
    print("-" * 40)