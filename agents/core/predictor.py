# agents/core/predictor.py

from datetime import datetime
from collections import defaultdict
from agents.tools.tools import get_customer_history


def analyze_refill_opportunity(customer_id: str):

    history = get_customer_history(customer_id)

    if history.get("status") != "ok":
        return {"refill_suggestion": False}

    orders = history.get("orders", [])

    if not orders or len(orders) < 2:
        return {"refill_suggestion": False}

    # ------------------------------------
    # Group orders by medicine
    # ------------------------------------
    medicine_dates = defaultdict(list)

    for order in orders:
        medicine = order.get("medicine")
        date_str = order.get("date")

        if medicine and date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                medicine_dates[medicine].append(date_obj)
            except:
                continue

    # ------------------------------------
    # Analyze each medicine pattern
    # ------------------------------------
    for medicine, dates in medicine_dates.items():

        if len(dates) < 2:
            continue

        dates.sort(reverse=True)

        # Calculate average gap
        gaps = []
        for i in range(len(dates) - 1):
            gap_days = (dates[i] - dates[i + 1]).days
            gaps.append(gap_days)

        if not gaps:
            continue

        avg_gap = sum(gaps) / len(gaps)

        # Current gap
        last_order_date = dates[0]
        today = datetime.now()
        current_gap = (today - last_order_date).days

        # ------------------------------------
        # Decision Logic
        # ------------------------------------
        # If current gap is >= 80% of average gap → suggest refill
        if avg_gap > 0 and current_gap >= (0.8 * avg_gap):

            return {
                "refill_suggestion": True,
                "medicine": medicine,
                "confidence": "high" if current_gap >= avg_gap else "medium",
                "reason": f"User typically refills every {round(avg_gap)} days. Last refill was {current_gap} days ago."
            }

    return {"refill_suggestion": False}