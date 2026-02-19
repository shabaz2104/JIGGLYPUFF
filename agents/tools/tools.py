import requests

BASE_URL = "https://destiny-nonaccordant-davina.ngrok-free.dev"


# ===============================
# CHECK INVENTORY
# ===============================
def check_inventory(medicine_name: str):
    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{medicine_name}",
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }


# ===============================
# CREATE ORDER
# ===============================
def create_order(customer_id: str, medicine: str, quantity: int):
    try:
        response = requests.post(
            f"{BASE_URL}/create-order",
            json={
                "customer_id": customer_id,
                "medicine": medicine,
                "quantity": quantity
            },
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }


# ===============================
# CUSTOMER HISTORY
# ===============================
def get_customer_history(customer_id: str):
    try:
        response = requests.get(
            f"{BASE_URL}/customer-history/{customer_id}",
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }


# ===============================
# UPDATE STOCK
# ===============================
def update_stock(medicine_name: str, stock: int):
    try:
        response = requests.post(
            f"{BASE_URL}/update-stock",
            json={
                "medicine": medicine_name,
                "stock": stock
            },
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }
