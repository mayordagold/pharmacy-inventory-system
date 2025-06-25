import sqlite3
import csv
import os
from tkinter import messagebox
import app

# Use the shared database path from your app backend
db_path = app.db_path

# Default export location
export_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory_export.csv"

def export_inventory(username, role):
    if role != "admin":
        messagebox.showerror("Permission Denied", "Only admins can export the inventory.")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve product data
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        # Write to CSV
        with open(export_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        # Notify success
        messagebox.showinfo("✅ Export Successful", f"Inventory exported to:\n{export_path}")
        print(f"✅ Exported to {export_path}")

    except Exception as e:
        messagebox.showerror("Export Failed", f"An error occurred while exporting:\n{e}")
        print(f"❌ Export failed: {e}")