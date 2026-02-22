# agents/core/predictor.py

import csv
import os
from datetime import datetime
from agents.tools.tools import get_customer_history

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


def analyze_refill_opportunity(customer_id: str):
    history = get_customer_history(customer_id)

    if history.get("status") != "ok":
        return {"refill_suggestion": False}

    orders = history.get("orders", [])

    if not orders:
        return {"refill_suggestion": False}

    latest_order = orders[0]

    medicine = latest_order.get("medicine")
    date_str = latest_order.get("date")

    if not medicine or not date_str:
        return {"refill_suggestion": False}

    rules = _load_rules()
    medicine_key = medicine.strip().lower()

    if medicine_key not in rules:
        return {"refill_suggestion": False}

    refill_days = int(rules[medicine_key]["refill_days"])

    try:
        order_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return {"refill_suggestion": False}

    days_since_order = (datetime.now() - order_date).days

    if days_since_order >= refill_days:
        return {
            "refill_suggestion": True,
            "medicine": medicine
        }

    return {"refill_suggestion": False}


def check_monthly_limit(customer_id: str, medicine_name: str, requested_quantity: int):

    if not medicine_name:
        return {"allowed": True}

    rules = _load_rules()
    medicine_key = medicine_name.strip().lower()

    if medicine_key not in rules:
        return {"allowed": True}

    max_limit = int(rules[medicine_key]["max_monthly_quantity"])

    history = get_customer_history(customer_id)

    if history.get("status") != "ok":
        return {"allowed": True}

    orders = history.get("orders", [])

    current_month = datetime.now().month
    current_year = datetime.now().year

    total_this_month = 0

    for order in orders:
        if order.get("medicine") and medicine_key in order.get("medicine").lower():
            date_str = order.get("date")

            if not date_str:
                continue

            try:
                order_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except Exception:
                continue

            if order_date.month == current_month and order_date.year == current_year:
                total_this_month += int(order.get("quantity", 0))

    if total_this_month + requested_quantity > max_limit:
        return {
            "allowed": False,
            "max_limit": max_limit,
            "current_usage": total_this_month
        }

    return {"allowed": True}