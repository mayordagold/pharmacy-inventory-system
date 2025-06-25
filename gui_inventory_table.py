import tkinter as tk
from tkinter import ttk
import sqlite3
import app  # ✅ To access db_path and log_user_action
from gui_utils import add_footer  # ✅ Reusable footer function

def show_inventory_window(username):
    def load_inventory():
        for row in table.get_children():
            table.delete(row)

        conn = sqlite3.connect(app.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, name, category, quantity_in_stock, price, expiry_date
            FROM products
            ORDER BY name ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            table.insert("", tk.END, values=row)

    # ✅ Log the user activity
    app.log_user_action(username, "Viewed inventory list")

    win = tk.Toplevel()
    win.title("📋 Inventory List")
    win.geometry("750x480")
    win.configure(bg="white")

    columns = ("ID", "Name", "Category", "Quantity", "Price", "Expiry")
    table = ttk.Treeview(win, columns=columns, show="headings", height=18)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=100 if col == "ID" else 120)

    table.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Button(
        win,
        text="🔄 Refresh",
        command=load_inventory,
        bg="#3498DB",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15
    ).pack(pady=10)

    # ✅ Add footer
    add_footer(win)

    load_inventory()