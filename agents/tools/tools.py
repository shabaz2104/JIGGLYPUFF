import requests
import os

BASE_URL = "http://localhost:5000"  # change if backend runs on different port

def check_stock(medicine_name: str, quantity: int):
    
    # MOCK RESPONSE (temporary)
    return {
        "status": "approved",
        "medicine_name": medicine_name,
        "available_quantity": 10,
        "requested_quantity": quantity
    }

    return response.json()


def create_order(order_data: dict):
    
    return {
        "status": "success",
        "order_id": "ORD123",
        "message": "Order created successfully"
    }


    return response.json()


def get_customer_history(customer_id: int):
    """
    Fetch customer purchase history.
    """
    response = requests.get(
        f"{BASE_URL}/customer-history/{customer_id}"
    )

    return response.json()
