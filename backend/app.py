from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db import get_db

app = Flask(__name__)
CORS(app)   # 👈 REQUIRED
# -------------------------------------------------
# INVENTORY CHECK
# -------------------------------------------------
@app.route("/inventory/<medicine>", methods=["GET"])
def check_inventory(medicine):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, price, stock
        FROM medicines
        WHERE name LIKE ?
        LIMIT 1
    """, (f"%{medicine}%",))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({
            "status": "not_found",
            "medicine": medicine
        }), 404

    return jsonify({
        "status": "ok",
        "medicine": row["name"],
        "price": row["price"],
        "stock": row["stock"],
        "available": row["stock"] > 0
    })



# -------------------------------------------------
# CREATE ORDER (FINAL, REAL LOGIC)
# -------------------------------------------------
@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json()

    customer_id = data.get("customer_id")
    medicine = data.get("medicine")
    quantity = data.get("quantity")

    # 1️⃣ Validate input
    if not all([customer_id, medicine, quantity]):
        return jsonify({
            "status": "error",
            "reason": "missing_fields"
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    # 2️⃣ Fetch medicine safely (ID-based)
    cursor.execute("""
        SELECT id, name, stock, price
        FROM medicines
        WHERE name LIKE ?
        LIMIT 1
    """, (f"%{medicine}%",))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({
            "status": "rejected",
            "reason": "medicine_not_found"
        }), 404

    if row["stock"] < quantity:
        conn.close()
        return jsonify({
            "status": "rejected",
            "reason": "insufficient_stock",
            "available_stock": row["stock"]
        }), 400

    # 3️⃣ Reduce stock (SAFE: using medicine ID)
    cursor.execute("""
        UPDATE medicines
        SET stock = stock - ?
        WHERE id = ?
    """, (quantity, row["id"]))

    # 4️⃣ Create order
    cursor.execute("""
        INSERT INTO orders (
            customer_id,
            product_name,
            quantity,
            purchase_date,
            total_price
        ) VALUES (?, ?, ?, datetime('now'), ?)
    """, (
        customer_id,
        row["name"],
        quantity,
        row["price"] * quantity
    ))

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "status": "created",
        "order_id": order_id,
        "medicine": row["name"],
        "quantity": quantity
    }), 201

# -------------------------------------------------
# CUSTOMER ORDER HISTORY
# -------------------------------------------------
@app.route("/customer-history/<user_id>", methods=["GET"])
def customer_history(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_name, quantity, purchase_date
        FROM orders
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    orders = []
    for row in rows:
        orders.append({
            "medicine": row["product_name"],
            "quantity": row["quantity"],
            "date": row["purchase_date"]
        })

    return jsonify({
        "status": "ok",
        "orders": orders
    })


# -------------------------------------------------
# UPDATE STOCK (FINAL, REAL LOGIC)
# -------------------------------------------------
@app.route("/update-stock", methods=["POST"])
def update_stock():
    data = request.get_json()

    medicine = data.get("medicine")
    delta = data.get("delta")  # can be + or -

    if medicine is None or delta is None:
        return jsonify({
            "status": "error",
            "reason": "missing_fields"
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    # 1️⃣ Fetch medicine safely
    cursor.execute("""
        SELECT id, name, stock
        FROM medicines
        WHERE name LIKE ?
        LIMIT 1
    """, (f"%{medicine}%",))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({
            "status": "rejected",
            "reason": "medicine_not_found"
        }), 404

    new_stock = row["stock"] + delta

    if new_stock < 0:
        conn.close()
        return jsonify({
            "status": "rejected",
            "reason": "stock_cannot_be_negative",
            "current_stock": row["stock"]
        }), 400

    # 2️⃣ Update stock by ID
    cursor.execute("""
        UPDATE medicines
        SET stock = ?
        WHERE id = ?
    """, (new_stock, row["id"]))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "updated",
        "medicine": row["name"],
        "stock": new_stock
    }), 200

# -------------------------------------------------
# SERVER START
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)