from agents.core.extractor import extract_order

test_input = "I need 4 strips of paracetamol"

order = extract_order(test_input)

print(order)
