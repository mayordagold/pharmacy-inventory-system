import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt  # type: ignore
from collections import defaultdict
from datetime import datetime
from tkinter import filedialog, simpledialog
from gui_utils import add_footer  # ✅ Reusable footer

db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

def show_analytics_window():
    win = tk.Toplevel()
    win.title("📊 Inventory Analytics")
    win.geometry("400x300")
    win.configure(bg="white")

    tk.Label(win, text="Analytics Dashboard", font=("Arial", 14, "bold"), bg="white", fg="#2C3E50").pack(pady=10)

    tk.Button(win, text="Top 5 Selling Products", width=30, command=show_top_sellers).pack(pady=5)
    tk.Button(win, text="Low Stock Alerts", width=30, command=show_low_stock).pack(pady=5)
    tk.Button(win, text="Monthly Sales Trend", width=30, command=show_monthly_trend).pack(pady=5)

    add_footer(win)  # ✅ Add footer at the bottom

def show_top_sellers():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, SUM(ABS(quantity_change)) AS total_sold
        FROM transactions
        WHERE action = 'sale'
        GROUP BY product_id
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "No sales data available.")
        return

    product_ids = [str(row[0]) for row in data]
    totals = [row[1] for row in data]

    plt.figure(figsize=(6, 4))
    plt.bar(product_ids, totals, color='skyblue')
    plt.title("Top 5 Selling Products")
    plt.xlabel("Product ID")
    plt.ylabel("Quantity Sold")
    plt.tight_layout()
    plt.show()

def show_low_stock():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, name, quantity_in_stock FROM products WHERE quantity_in_stock < 10
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("All Good", "No products are low in stock.")
        return

    product_names = [f"{row[1]} ({row[0]})" for row in data]
    quantities = [row[2] for row in data]

    plt.figure(figsize=(6, 4))
    plt.barh(product_names, quantities, color='tomato')
    plt.title("Low Stock Products (Qty < 10)")
    plt.xlabel("Quantity Remaining")
    plt.tight_layout()
    plt.show()

def show_monthly_trend():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, ABS(quantity_change)
        FROM transactions
        WHERE action = 'sale'
    """)
    data = cursor.fetchall()
    conn.close()

    monthly_sales = defaultdict(int)
    for ts, qty in data:
        month = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m")
        monthly_sales[month] += qty

    if not monthly_sales:
        messagebox.showinfo("No Data", "No sales trend data available.")
        return

    months = sorted(monthly_sales.keys())
    totals = [monthly_sales[m] for m in months]

    plt.figure(figsize=(6, 4))
    plt.plot(months, totals, marker='o', color='green')
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Quantity Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()