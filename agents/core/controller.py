from agents.models.schemas import MedicineOrder
from agents.tools.tools import (
    check_inventory,
    create_order,
    get_customer_history
)


def process_order(order: MedicineOrder):

    # Step 1 — Check inventory
    inventory_response = check_inventory(order.medicine_name)

    if inventory_response.get("status") != "available":
        return {
            "status": "rejected",
            "reason": "Medicine not available"
        }

    # Step 2 — Create order
    order_response = create_order(
        customer_id="PAT001",  # For now fixed (we improve later)
        medicine_name=order.medicine_name,
        quantity=order.quantity
    )

    if order_response.get("status") != "created":
        return {
            "status": "error",
            "reason": "Order creation failed"
        }

    return {
        "status": "success",
        "order_id": order_response.get("order_id")
    }
