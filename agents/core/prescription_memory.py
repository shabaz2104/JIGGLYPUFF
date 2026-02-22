# agents/core/prescription_memory.py

_verified_prescriptions = {}


def mark_prescription_verified(customer_id: str, medicine_name: str):

    key = f"{customer_id}_{medicine_name.lower()}"
    _verified_prescriptions[key] = True


def is_prescription_verified(customer_id: str, medicine_name: str):

    key = f"{customer_id}_{medicine_name.lower()}"
    return _verified_prescriptions.get(key, False)