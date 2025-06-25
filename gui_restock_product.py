import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
from gui_utils import add_footer

db_path = "C:/Users/USER/OneDrive/Desktop/pharmacy-inventory-system/inventory.db"

def submit_restock(fields, username):
    name = fields["Product Name"].get().strip().lower()
    try:
        new_price = float(fields["Price"].get().strip())
        qty_to_add = int(fields["Quantity to Add"].get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Price must be a number and quantity must be an integer.")
        return

    category = fields["Category"].get().strip()
    supplier = fields["Supplier"].get().strip()
    expiry_str = fields["Expiry Date"].get()

    if not name:
        messagebox.showerror("Missing Info", "Product name cannot be empty.")
        return

    if expiry_str:
        try:
            datetime.strptime(expiry_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Expiry date must be in YYYY-MM-DD format.")
            return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT product_id FROM products WHERE LOWER(name) = ?", (name,))
    row = cursor.fetchone()

    if not row:
        messagebox.showerror("Product Not Found", f"No existing product named '{name}' was found.")
        conn.close()
        return

    product_id = row[0]

    cursor.execute("""
        UPDATE products
        SET price = ?, quantity_in_stock = quantity_in_stock + ?,
            category = ?, expiry_date = ?, supplier_name = ?
        WHERE product_id = ?
    """, (new_price, qty_to_add, category, expiry_str, supplier, product_id))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transactions (product_id, quantity_change, action, timestamp, username)
        VALUES (?, ?, 'restock', ?, ?)
    """, (product_id, qty_to_add, timestamp, username))

    conn.commit()
    conn.close()

    messagebox.showinfo("✅ Restocked", f"Updated '{name}' with +{qty_to_add} units.")

    for field in fields.values():
        if isinstance(field, (tk.Entry, ttk.Combobox)):
            field.delete(0, tk.END)
        elif isinstance(field, DateEntry):
            field.set_date(datetime.today())

def show_restock_window(username, role):
    win = tk.Toplevel()
    win.title("📦 Product Restock")
    win.geometry("370x560")
    win.configure(bg="white")

    fields = {}

    def add_labeled_widget(label_text, widget):
        tk.Label(win, text=label_text, bg="white", anchor="w", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor="w")
        widget.pack(pady=2)
        fields[label_text] = widget

    # Load product names from database for dropdown
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products ORDER BY name ASC")
        product_names = [row[0] for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        product_names = []
        print("⚠️ Could not load product names:", e)

    # Product Name Dropdown
    product_cb = ttk.Combobox(win, values=product_names, width=32)
    add_labeled_widget("Product Name", product_cb)

    add_labeled_widget("Price", tk.Entry(win, width=35))
    add_labeled_widget("Quantity to Add", tk.Entry(win, width=35))

    category_options = ["Analgesic", "Antibiotic", "Antacid", "Antifungal", "Supplement", "Vaccine", "Other"]
    category_cb = ttk.Combobox(win, values=category_options, width=32, state="readonly")
    add_labeled_widget("Category", category_cb)

    expiry_picker = DateEntry(win, width=33, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    add_labeled_widget("Expiry Date", expiry_picker)

    supplier_options = ["GSK", "Pfizer", "Neimeth", "Meyer", "Jawa", "Others"]
    supplier_cb = ttk.Combobox(win, values=supplier_options, width=32)
    add_labeled_widget("Supplier", supplier_cb)

    tk.Button(
        win,
        text="Submit Restock",
        command=lambda: submit_restock(fields, username),
        bg="#27AE60",
        fg="white",
        font=("Arial", 11, "bold"),
        width=25
    ).pack(pady=25)

    add_footer(win)