import tkinter as tk
from tkinter import messagebox
import sqlite3
from gui_utils import add_footer  # ✅ Reusable footer

db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

def load_transactions(listbox):
    listbox.delete(0, tk.END)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, quantity_change, action, timestamp, username
        FROM transactions
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        listbox.insert(tk.END, "No transaction history available.")
    else:
        for row in rows:
            label = f"[{row[3]}] | {row[4]} | {row[2].capitalize()} | Product ID: {row[0]} | Qty: {row[1]}"
            listbox.insert(tk.END, label)

def show_transaction_history():
    win = tk.Toplevel()
    win.title("🧾 Transaction History")
    win.geometry("600x400")
    win.configure(bg="white")

    listbox = tk.Listbox(win, width=90, height=20)
    listbox.pack(pady=10)

    tk.Button(win, text="🔄 Refresh", command=lambda: load_transactions(listbox)).pack(pady=5)

    add_footer(win)  # ✅ Add footer at the bottom

    load_transactions(listbox)