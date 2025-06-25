import tkinter as tk
from tkinter import messagebox
import sqlite3
from gui_utils import add_footer  # ✅ Reusable footer

# Path to your inventory database
db_path = "C:/Users/USER/OneDrive/Desktop/chemist-inventory/inventory.db"

def submit_product(entries):
    name = entries["Name"].get().strip()
    category = entries["Category"].get().strip()
    try:
        quantity = int(entries["Quantity"].get().strip())
        price = float(entries["Price"].get().strip())
    except ValueError:
        messagebox.showerror("Invalid input", "Quantity must be an integer and price must be a number.")
        return

    expiry = entries["Expiry (YYYY-MM-DD)"].get().strip()
    supplier = entries["Supplier"].get().strip()

    if not name or not expiry:
        messagebox.showwarning("Missing info", "Name and expiry date are required.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for duplicate product name (case-insensitive)
    cursor.execute("SELECT 1 FROM products WHERE LOWER(name) = ?", (name.lower(),))
    if cursor.fetchone():
        messagebox.showerror("Duplicate Product", f"A product named '{name}' already exists.")
        conn.close()
        return

    try:
        cursor.execute("""
            INSERT INTO products (name, category, quantity_in_stock, price, expiry_date, supplier_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, quantity, price, expiry, supplier))
        conn.commit()
        messagebox.showinfo("Success", f"✅ Product '{name}' added to inventory.")
        for field in entries.values():
            field.delete(0, tk.END)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

def show_add_product_window(username):
    win = tk.Toplevel()
    win.title("➕ Add New Product")
    win.geometry("350x400")
    win.configure(bg="white")

    fields = ["Name", "Category", "Quantity", "Price", "Expiry (YYYY-MM-DD)", "Supplier"]
    entries = {}

    for field in fields:
        tk.Label(win, text=field, bg="white").pack(pady=2)
        entry = tk.Entry(win)
        entry.pack(pady=2)
        entries[field] = entry

    tk.Button(win, text="Submit", command=lambda: submit_product(entries), bg="#2ECC71", fg="white").pack(pady=20)

    add_footer(win)  # ✅ Add footer at the bottom