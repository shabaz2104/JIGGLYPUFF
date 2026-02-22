# agents/core/memory.py

_memory_store = {}

def save_last_medicine(customer_id: str, medicine_name: str):
    if not customer_id:
        customer_id = "PAT001"
    _memory_store[customer_id] = medicine_name


def get_last_medicine(customer_id: str):
    if not customer_id:
        customer_id = "PAT001"
    return _memory_store.get(customer_id)