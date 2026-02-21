import sqlite3

DB_NAME = "pharmacy.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # ---------------------------------
    # Medicines table (with REAL stock)
    # ---------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER DEFAULT 0,
        package_size TEXT,
        description TEXT,
        pzn TEXT
    )
    """)

    # -----------------
    # Customers table
    # -----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        age INTEGER,
        gender TEXT
    )
    """)

    # --------------
    # Orders table
    # --------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        product_name TEXT,
        quantity INTEGER,
        purchase_date TEXT,
        total_price REAL,
        dosage_frequency TEXT,
        prescription_required TEXT
    )
    """)

    conn.commit()
    conn.close()