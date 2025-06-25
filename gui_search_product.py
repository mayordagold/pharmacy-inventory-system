import tkinter as tk
from tkinter import messagebox
import sqlite3
from gui_utils import add_footer  # ✅ Reusable footer

db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

def search_products(entry, result_list):
    keyword = entry.get().strip()
    result_list.delete(0, tk.END)

    if not keyword:
        messagebox.showinfo("Input Needed", "Enter product name or category to search.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, name, category, quantity_in_stock, price, expiry_date, supplier_name
        FROM products
        WHERE name LIKE ? OR category LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        result_list.insert(tk.END, "No matching products found.")
    else:
        for row in rows:
            info = f"ID: {row[0]} | {row[1]} ({row[2]}) | Stock: {row[3]} | ₦{row[4]:.2f} | Exp: {row[5]}"
            result_list.insert(tk.END, info)

def show_search_window():
    win = tk.Toplevel()
    win.title("🔍 Search Products")
    win.geometry("500x400")
    win.configure(bg="white")

    tk.Label(win, text="Enter keyword (name/category):", bg="white").pack(pady=5)
    entry = tk.Entry(win, width=40)
    entry.pack(pady=5)

    result_list = tk.Listbox(win, width=70, height=15)
    result_list.pack(pady=10)

    tk.Button(win, text="Search", command=lambda: search_products(entry, result_list)).pack(pady=10)

    add_footer(win)  # ✅ Add footer at the bottom