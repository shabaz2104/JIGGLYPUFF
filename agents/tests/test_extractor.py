from agents.core.extractor import extract_order

if __name__ == "__main__":
    test_input = "Order 2 Crocin"
    order = extract_order(test_input)
    print(order)
