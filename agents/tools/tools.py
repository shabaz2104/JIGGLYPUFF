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