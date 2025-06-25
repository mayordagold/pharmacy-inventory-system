import sqlite3
import hashlib
from datetime import datetime

# === Database Path ===
db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

# === Hash Utility ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# === Initialize Database and Default Users ===
def setup_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity_in_stock INTEGER,
            price REAL,
            expiry_date TEXT,
            supplier_name TEXT
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity_change INTEGER,
            action TEXT,
            timestamp TEXT,
            username TEXT,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );

        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'sales_user'))
        );

        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            timestamp TEXT
        );
    """)
    default_users = [
        ("admin_user", hash_password("admin123"), "admin"),
        ("sales_user1", hash_password("sales123"), "sales_user")
    ]
    for user in default_users:
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", user)
    conn.commit()
    conn.close()
    print("✅ Database setup complete. Default users ensured.")

# === Log User Action ===
def log_user_action(username, action):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO activity_logs (username, action, timestamp) VALUES (?, ?, ?)",
        (username, action, timestamp)
    )
    conn.commit()
    conn.close()

# === Inventory & Transaction Operations ===
def view_inventory():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} ({row[2]}) | Qty: {row[3]} | ₦{row[4]} | Exp: {row[5]} | Supplier: {row[6]}")
    else:
        print("❌ Inventory is empty.")

def add_product():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("\n➕ Add New Product")
    name = input("Product Name: ").strip()
    category = input("Category: ").strip()
    quantity_in_stock = int(input("Quantity in Stock: "))
    price = float(input("Price (₦): "))
    expiry_date = input("Expiry Date (YYYY-MM-DD): ").strip()
    supplier_name = input("Supplier Name: ").strip()
    cursor.execute("""
        INSERT INTO products (name, category, quantity_in_stock, price, expiry_date, supplier_name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, quantity_in_stock, price, expiry_date, supplier_name))
    conn.commit()
    conn.close()
    print("✅ Product added successfully.")

def search_product():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    term = input("Search by name, category, or supplier: ").strip().lower()
    cursor.execute("""
        SELECT * FROM products
        WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(supplier_name) LIKE ?
    """, (f"%{term}%", f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} ({row[2]}) | Qty: {row[3]} | ₦{row[4]} | Exp: {row[5]} | Supplier: {row[6]}")
    else:
        print("❌ No matches found.")

def update_stock(product_id, quantity_change):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity_in_stock FROM products WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()
    if not result:
        print("❌ Product not found.")
        conn.close()
        return False
    new_qty = result[0] + quantity_change
    if new_qty < 0:
        print("❌ Not enough stock.")
        conn.close()
        return False
    cursor.execute("UPDATE products SET quantity_in_stock = ? WHERE product_id = ?", (new_qty, product_id))
    conn.commit()
    conn.close()
    print("✅ Stock updated.")
    return True

def record_transaction_action(username, action):
    product_id = int(input(f"Product ID for {action}: "))
    qty = int(input(f"Quantity {action}: "))
    quantity_change = -qty if action == "sale" else qty
    if update_stock(product_id, quantity_change):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO transactions (product_id, quantity_change, action, timestamp, username)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, quantity_change, action, timestamp, username))
        conn.commit()
        conn.close()
        print(f"✅ {action.capitalize()} recorded.")
        log_user_action(username, f"{action.capitalize()} - Product ID {product_id} Qty {qty}")

def view_transaction_history():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    pid = input("Filter by product ID (or press Enter to skip): ").strip()
    action = input("Filter by action (sale/restock or press Enter to skip): ").strip().lower()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if pid:
        query += " AND product_id = ?"
        params.append(pid)
    if action in ['sale', 'restock']:
        query += " AND action = ?"
        params.append(action)
    query += " ORDER BY timestamp DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(f"[{row[4]}] User: {row[5]} | Product ID: {row[1]} | {row[3].upper()} | Qty: {row[2]}")
    else:
        print("❌ No transactions found.")

def create_sales_user():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("\n👤 Create New Sales User")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, "sales_user"))
        conn.commit()
        print(f"✅ Sales user '{username}' created.")
        log_user_action("admin_user", f"Created new sales user: {username}")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    conn.close()

# === GUI Dashboard Entry ===
def launch_dashboard(username, role):
    try:
        import gui_dashboard
        gui_dashboard.launch_dashboard(username, role)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")

# === App Entry Point ===
if __name__ == "__main__":
    setup_database()
    from gui_login import show_login
    show_login()