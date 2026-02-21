# agents/core/prescription_rules.py

# Temporary rule set
# In hackathon, you can load this from CSV later

PRESCRIPTION_REQUIRED = {
    "amoxicillin": True,
    "insulin": True,
    "morphine": True,
    "paracetamol": False,
    "ibuprofen": False,
}


def requires_prescription(medicine_name: str) -> bool:
    if not medicine_name:
        return False

    name = medicine_name.lower()

    for key in PRESCRIPTION_REQUIRED:
        if key in name:
            return PRESCRIPTION_REQUIRED[key]

    return False