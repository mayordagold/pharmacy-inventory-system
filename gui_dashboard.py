import tkinter as tk
from tkinter import messagebox
import app  # Backend core logic
import sqlite3
from datetime import datetime, timedelta

from gui_create_admin_user import show_create_admin_user_window
from export_inventory import export_inventory
from gui_add_product import show_add_product_window
from gui_record_sale import show_sale_window
from gui_restock_product import show_restock_window
from gui_search_product import show_search_window
from gui_transaction_history import show_transaction_history
from gui_analytics import show_analytics_window
from gui_inventory_table import show_inventory_window
from gui_create_sales_user import show_create_user_window
from gui_view_logs import show_activity_log_window

# === Check for Expiring or Expired Products ===
def check_expiring_products(threshold_days=30):
    conn = sqlite3.connect(app.db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, expiry_date, quantity_in_stock FROM products
        WHERE expiry_date IS NOT NULL AND expiry_date != ''
    """)
    today = datetime.today().date()
    soon_to_expire = []

    for name, exp_str, qty in cursor.fetchall():
        try:
            exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
            days_left = (exp_date - today).days
            if days_left <= threshold_days:
                soon_to_expire.append((name, exp_str, qty, days_left))
        except Exception:
            continue

    conn.close()
    return soon_to_expire

# === Launch Dashboard ===
def launch_dashboard(username="admin", role="admin"):
    print("🚀 Launching Dashboard...")

    expiring = check_expiring_products()
    if expiring:
        msg = "⚠️ The following products are expired or near expiry:\n\n"
        for name, exp, qty, days in expiring:
            if days >= 0:
                msg += f"• {name} (Qty: {qty}) – Expires in {days} day(s) [{exp}]\n"
            else:
                msg += f"• {name} (Qty: {qty}) – ❌ Expired {abs(days)} day(s) ago [{exp}]\n"
        messagebox.showwarning("Expiry Alert", msg)

    dash = tk.Tk()
    dash.title("💼 ONYXCARE Inventory Dashboard")
    dash.geometry("500x600")
    dash.configure(bg="#2C3E50")

    header = tk.Label(
        dash,
        text=f"Welcome {username} ({role})",
        font=("Arial", 15, "bold"),
        fg="white",
        bg="#34495E"
    )
    header.pack(pady=12, fill="x")

    button_style = {
        "font": ("Arial", 11),
        "bg": "#3498DB",
        "fg": "white",
        "activebackground": "#2980B9",
        "activeforeground": "white",
        "width": 26,
        "height": 1
    }

    button_frame = tk.Frame(dash, bg="#2C3E50")
    button_frame.pack(pady=5)

    # === Admin-only buttons ===
    if role == "admin":
        tk.Button(button_frame, text="📦 Add Product", command=lambda: show_add_product_window(username), **button_style).pack(pady=3)
        tk.Button(button_frame, text="📊 Analytics", command=show_analytics_window, **button_style).pack(pady=3)
        tk.Button(button_frame, text="📥 Product Restock", command=lambda: show_restock_window(username, role), **button_style).pack(pady=3)
        tk.Button(button_frame, text="👤 Create Sales User", command=show_create_user_window, **button_style).pack(pady=3)
        tk.Button(button_frame, text="📤 Export Inventory", command=lambda: export_inventory(username, role), **button_style).pack(pady=3)
        tk.Button(button_frame, text="📜 View Activity Log", command=show_activity_log_window, **button_style).pack(pady=3)
        tk.Button(button_frame, text="👑 Create Admin User", command=lambda: show_create_admin_user_window(username), **button_style).pack(pady=3)

    # === Shared Features ===
    tk.Button(
        dash,
        text="📋 View Inventory",
        command=lambda: show_inventory_window(username),
        font=("Arial", 11),
        bg="#1ABC9C",
        fg="white",
        width=22,
        height=1
    ).pack(pady=10)

    tk.Button(button_frame, text="🔎 Search Product", command=show_search_window, **button_style).pack(pady=3)
    tk.Button(button_frame, text="🛒 Record Sale", command=lambda: show_sale_window(username), **button_style).pack(pady=3)
    tk.Button(button_frame, text="🧾 Transaction History", command=show_transaction_history, **button_style).pack(pady=3)

    # === Logout (with logging) ===
    def logout():
        app.log_user_action(username, "Logged out")
        dash.destroy()
        print("👋 Logged out. See you soon!")
        from gui_login import show_login
        show_login()

    tk.Button(
        dash,
        text="🚪 Logout",
        command=logout,
        font=("Arial", 11, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#C0392B",
        activeforeground="white",
        width=14,
        height=1
    ).pack(pady=15)

     # === Footer ===
    footer = tk.Label(
        dash,
        text="© 2025 Olumayowa A. | Licensed under the MIT License",
        font=("Arial", 9),
        fg="white",
        bg="#2C3E50"
    )
    footer.pack(side="bottom", pady=5)

    print("✅ Dashboard Loaded Successfully!")
    dash.mainloop()


if __name__ == "__main__":
    launch_dashboard()