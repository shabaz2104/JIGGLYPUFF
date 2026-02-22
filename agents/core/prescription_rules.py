# agents/core/prescription_rules.py

import csv
import os

RULES_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "medicine_rules.csv"
)


def _load_rules():
    rules = {}

    with open(RULES_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            medicine = row["medicine"].strip().lower()
            rules[medicine] = row

    return rules


def requires_prescription(medicine_name: str) -> bool:

    if not medicine_name:
        return False

    rules = _load_rules()

    medicine_key = medicine_name.strip().lower()

    if medicine_key in rules:
        return rules[medicine_key]["prescription_required"].lower() == "true"

    return False


PRESCRIPTION_REQUIRED_MEDICINES = {
    "amoxicillin",
    "azithromycin",
    "alprazolam",
    "clonazepam",
    "metformin"
}


def requires_prescription(medicine_name: str) -> bool:

    if not medicine_name:
        return False

    return medicine_name.lower() in PRESCRIPTION_REQUIRED_MEDICINES