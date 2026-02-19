from agents.tools.tools import (
    check_inventory,
    create_order,
    get_customer_history,
    update_stock
)


def handle_intent(request):

    intent = request.intent

    # =========================
    # ORDER
    # =========================
    if intent == "order":

        if not request.medicine_name or not request.quantity:
            return {
                "status": "error",
                "reason": "missing_fields"
            }

        inventory = check_inventory(request.medicine_name)

        if inventory.get("status") != "available":
            return {
                "status": "rejected",
                "reason": "medicine_not_found"
            }

        return create_order(
            customer_id=request.customer_id or "PAT001",
            medicine=request.medicine_name,
            quantity=request.quantity
        )

    # =========================
    # INVENTORY
    # =========================
    elif intent == "inventory":

        if not request.medicine_name:
            return {
                "status": "error",
                "reason": "missing_medicine_name"
            }

        return check_inventory(request.medicine_name)

    # =========================
    # HISTORY
    # =========================
    elif intent == "history":

        return get_customer_history(request.customer_id or "PAT001")

    # =========================
    # UPDATE STOCK
    # =========================
    elif intent == "update_stock":

        if not request.medicine_name or request.stock is None:
            return {
                "status": "error",
                "reason": "missing_fields"
            }

        return update_stock(
            request.medicine_name,
            request.stock
        )

    # =========================
    # UNKNOWN
    # =========================
    else:
        return {
            "status": "error",
            "reason": "unknown_intent"
        }
