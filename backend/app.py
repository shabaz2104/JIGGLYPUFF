from flask import Flask, jsonify
from database.db import get_db

app = Flask(__name__)

# -----------------------------
# MOCK MEDICINES API
# -----------------------------
@app.route("/mock/medicines", methods=["GET"])
def get_medicines():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, price, package_size, pzn
        FROM medicines
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    medicines = []
    for row in rows:
        medicines.append({
            "id": row["id"],
            "name": row["name"],
            "price": row["price"],
            "package_size": row["package_size"],
            "pzn": row["pzn"]
        })

    return jsonify({
        "status": "ok",
        "count": len(medicines),
        "data": medicines
    })


# -----------------------------
# MOCK CUSTOMERS API
# -----------------------------
@app.route("/mock/customers", methods=["GET"])
def get_customers():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, age, gender
        FROM customers
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    customers = []
    for row in rows:
        customers.append({
            "customer_id": row["id"],
            "age": row["age"],
            "gender": row["gender"]
        })

    return jsonify({
        "status": "ok",
        "count": len(customers),
        "data": customers
    })


if __name__ == "__main__":
    app.run(debug=True)