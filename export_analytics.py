import os
import sqlite3
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt  # type: ignore

db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

def export_all_charts():
    # Step 1: Create export folder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = os.path.join("analytics_exports", timestamp)
    os.makedirs(folder, exist_ok=True)

    export_top_sellers(folder)
    export_low_stock(folder)
    export_monthly_trend(folder)

    # Open the folder (Windows)
    os.startfile(folder)

def export_top_sellers(folder):
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

    if data:
        ids = [str(row[0]) for row in data]
        totals = [row[1] for row in data]

        plt.figure(figsize=(6,4))
        plt.bar(ids, totals, color="skyblue")
        plt.title("Top 5 Selling Products")
        plt.xlabel("Product ID")
        plt.ylabel("Quantity Sold")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "top_sellers.png"))
        plt.close()

def export_low_stock(folder):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, name, quantity_in_stock FROM products WHERE quantity_in_stock < 10
    """)
    data = cursor.fetchall()
    conn.close()

    if data:
        names = [f"{row[1]} ({row[0]})" for row in data]
        quantities = [row[2] for row in data]

        plt.figure(figsize=(6,4))
        plt.barh(names, quantities, color="tomato")
        plt.title("Low Stock Products (Qty < 10)")
        plt.xlabel("Quantity Remaining")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "low_stock.png"))
        plt.close()

def export_monthly_trend(folder):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, ABS(quantity_change)
        FROM transactions
        WHERE action = 'sale'
    """)
    data = cursor.fetchall()
    conn.close()

    monthly = defaultdict(int)
    for ts, qty in data:
        month = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m")
        monthly[month] += qty

    if monthly:
        months = sorted(monthly.keys())
        totals = [monthly[m] for m in months]

        plt.figure(figsize=(6,4))
        plt.plot(months, totals, marker="o", color="green")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Quantity Sold")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "monthly_trend.png"))
        plt.close()