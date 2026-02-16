import requests

BASE_URL = "http://127.0.0.1:5000"


def check_inventory(medicine_name: str):
    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{medicine_name}"
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def create_order(customer_id: str, medicine_name: str, quantity: int):
    try:
        response = requests.post(
            f"{BASE_URL}/create-order",
            json={
                "customer_id": customer_id,
                "medicine": medicine_name,
                "quantity": quantity
            }
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_customer_history(customer_id: str):
    try:
        response = requests.get(
            f"{BASE_URL}/customer-history/{customer_id}"
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
