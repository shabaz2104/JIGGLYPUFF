from agents.models.schemas import MedicineOrder
from agents.tools.tools import check_stock, create_order


def process_order(order: MedicineOrder):

    # Step 1 — Check stock
    stock_response = check_stock(
        order.medicine_name,
        order.quantity
    )

    # Step 2 — Decision logic
    if stock_response["status"] != "approved":
        return {
            "status": "rejected",
            "reason": "Medicine not available"
        }

    # Step 3 — Create order
    order_response = create_order(order.dict())

    return {
        "status": "success",
        "order_details": order_response
    }
