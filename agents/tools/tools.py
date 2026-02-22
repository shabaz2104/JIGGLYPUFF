 main
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

# agents/tools/tools.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://destiny-nonaccordant-davina.ngrok-free.dev"


def health_check():
    try:
        r = requests.get(f"{BASE_URL}/health")
        return r.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_inventory(medicine_name):
    try:
        r = requests.get(f"{BASE_URL}/inventory/{medicine_name}")
        return r.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def create_order(customer_id, medicine_name, quantity):
    try:
        r = requests.post(
            f"{BASE_URL}/create-order",
            json={
                "customer_id": customer_id,
                "medicine": medicine_name,
                "quantity": quantity
            }
        )
        return r.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def update_stock(medicine_name, delta):
    try:
        r = requests.post(
            f"{BASE_URL}/update-stock",
            json={
                "medicine": medicine_name,
                "delta": delta
            }
        )
        return r.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def get_customer_history(customer_id):
    try:
        r = requests.get(f"{BASE_URL}/customer-history/{customer_id}")
        return r.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}
 main
