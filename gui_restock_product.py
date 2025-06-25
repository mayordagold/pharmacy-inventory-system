import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from gui_utils import add_footer  # ✅ Reusable footer

db_path = "C:/Users/USER/OneDrive/Desktop/chemist-inventory/inventory.db"

def submit_restock(fields, username):
    name = fields["Product Name"].get().strip().lower()
    try:
        new_price = float(fields["Price"].get().strip())
        qty_to_add = int(fields["Quantity to Add"].get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Price must be a number and quantity must be an integer.")
        return

    if not name:
        messagebox.showerror("Missing Info", "Product name cannot be empty.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Look for matching product by name
    cursor.execute("SELECT product_id FROM products WHERE LOWER(name) = ?", (name,))
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Product Not Found", f"No existing product named '{name}' was found.")
        conn.close()
        return

    product_id = row[0]

    # Update product
    cursor.execute("""
        UPDATE products
        SET price = ?, quantity_in_stock = quantity_in_stock + ?
        WHERE product_id = ?
    """, (new_price, qty_to_add, product_id))

    # Log transaction
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transactions (product_id, quantity_change, action, timestamp, username)
        VALUES (?, ?, 'restock', ?, ?)
    """, (product_id, qty_to_add, timestamp, username))

    conn.commit()
    conn.close()

    messagebox.showinfo("✅ Restocked", f"Updated '{name}' with +{qty_to_add} units.")
    for field in fields.values():
        field.delete(0, tk.END)

def show_restock_window(username, role):
    win = tk.Toplevel()
    win.title("📦 Restock Existing Product")
    win.geometry("350x300")
    win.configure(bg="white")

    field_labels = ["Product Name", "Price", "Quantity to Add"]
    fields = {}

    for label in field_labels:
        tk.Label(win, text=label, bg="white").pack(pady=5)
        entry = tk.Entry(win, width=30)
        entry.pack()
        fields[label] = entry

    tk.Button(
        win, text="Submit Restock",
        command=lambda: submit_restock(fields, username),
        bg="#27AE60", fg="white"
    ).pack(pady=20)

    add_footer(win)  # ✅ Add footer at the bottom