import sys
from pathlib import Path
import pandas as pd

# -------------------------
# Fix Python path
# -------------------------
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from database.db import get_db

# -------------------------
# Excel file locations
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
PRODUCTS_FILE = BASE_DIR / "products-export.xlsx"
ORDERS_FILE = BASE_DIR / "Consumer Order History 1.xlsx"


# -------------------------
# IMPORT MEDICINES
# -------------------------
def import_medicines():
    df = pd.read_excel(PRODUCTS_FILE)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO medicines (
                id, name, price, package_size, description, pzn
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            int(row["product id"]),
            row["product name"],
            float(row["price rec"]),
            row["package size"],
            row["descriptions"],
            row["pzn"]
        ))

    conn.commit()
    conn.close()
    print(f"✅ Imported {len(df)} medicines")


# -------------------------
# IMPORT CUSTOMERS
# -------------------------
def import_customers():
    df = pd.read_excel(ORDERS_FILE, header=4)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers")

    seen = set()
    count = 0

    for _, row in df.iterrows():
        cid = row["Patient ID"]
        if cid in seen:
            continue

        cursor.execute("""
            INSERT INTO customers (id, age, gender)
            VALUES (?, ?, ?)
        """, (
            cid,
            int(row["Patient Age"]),
            row["Patient Gender"]
        ))

        seen.add(cid)
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ Imported {count} customers")


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    import_medicines()
    import_customers()
    print("🎉 FULL IMPORT DONE")