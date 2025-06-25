import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import app
from gui_utils import add_footer  # ✅ Make sure this is available

def show_sale_window(username):
    cart = []
    total_amount = tk.DoubleVar(value=0.0)
    live_subtotal = tk.StringVar(value="₦0.00")

    def search_product():
        search_term = entry_search.get().strip().lower()
        conn = sqlite3.connect(app.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, name, quantity_in_stock, price FROM products
            WHERE LOWER(name) LIKE ?
        """, (f"%{search_term}%",))
        results = cursor.fetchall()
        conn.close()

        listbox_results.delete(0, tk.END)
        for row in results:
            listbox_results.insert(tk.END, f"{row[0]} | {row[1]} | In Stock: {row[2]} | ₦{row[3]}")
        listbox_results.focus_set()

    def select_product(evt):
        if listbox_results.curselection():
            selection = listbox_results.get(listbox_results.curselection())
            parts = selection.split(" | ")
            selected_pid.set(parts[0])
            selected_name.set(parts[1])
            selected_price.set(parts[3].replace("₦", "").strip())
            label_price.config(text=f"Unit Price: ₦{float(selected_price.get()):,.2f}")
            entry_qty.delete(0, tk.END)
            live_subtotal.set("₦0.00")

    def update_total_label():
        total = sum(item["subtotal"] for item in cart)
        total_amount.set(total)
        label_total.config(text=f"Total: ₦{total:,.2f}")

    def update_live_subtotal(*args):
        try:
            qty = int(entry_qty.get())
            price = float(selected_price.get())
            sub = qty * price
            live_subtotal.set(f"Estimated: ₦{sub:,.2f}")
        except:
            live_subtotal.set("₦0.00")

    def refresh_cart_table():
        for item in cart_table.get_children():
            cart_table.delete(item)
        for i, item in enumerate(cart):
            cart_table.insert('', 'end', iid=str(i), values=(
                item["name"],
                item["quantity"],
                f"₦{item['price']:,.2f}",
                f"₦{item['subtotal']:,.2f}"
            ))
        update_total_label()

    def add_to_cart():
        pid = selected_pid.get()
        name = selected_name.get()
        price = selected_price.get()
        qty = entry_qty.get().strip()

        if not pid or not qty.isdigit():
            messagebox.showwarning("Missing Info", "Select a product and enter a valid quantity.")
            return

        qty = int(qty)
        price = float(price)
        subtotal = qty * price

        for item in cart:
            if item["product_id"] == pid:
                item["quantity"] += qty
                item["subtotal"] = item["quantity"] * item["price"]
                refresh_cart_table()
                entry_qty.delete(0, tk.END)
                live_subtotal.set("₦0.00")
                return

        cart.append({
            "product_id": pid,
            "name": name,
            "price": price,
            "quantity": qty,
            "subtotal": subtotal
        })

        refresh_cart_table()
        entry_qty.delete(0, tk.END)
        live_subtotal.set("₦0.00")

    def edit_cart_item():
        selected = cart_table.focus()
        if not selected:
            messagebox.showwarning("No selection", "Select an item in the cart to edit.")
            return
        index = int(selected)
        item = cart[index]
        new_qty = simpledialog.askinteger("Edit Quantity", f"Enter new quantity for {item['name']}:", initialvalue=item["quantity"])
        if new_qty is None:
            return
        if new_qty <= 0:
            cart.pop(index)
        else:
            item["quantity"] = new_qty
            item["subtotal"] = new_qty * item["price"]
        refresh_cart_table()

    def remove_cart_item():
        selected = cart_table.focus()
        if not selected:
            messagebox.showwarning("No selection", "Select an item to remove.")
            return
        index = int(selected)
        cart.pop(index)
        refresh_cart_table()

    def checkout():
        if not cart:
            messagebox.showwarning("Cart Empty", "No items in cart.")
            return

        conn = sqlite3.connect(app.db_path)
        cursor = conn.cursor()
        for item in cart:
            cursor.execute(
                "INSERT INTO transactions (product_id, quantity_change, action, timestamp, username) VALUES (?, ?, 'sale', datetime('now'), ?)",
                (item["product_id"], -item["quantity"], username)
            )
            cursor.execute(
                "UPDATE products SET quantity_in_stock = quantity_in_stock - ? WHERE product_id = ?",
                (item["quantity"], item["product_id"])
            )
        conn.commit()
        conn.close()

        app.log_user_action(username, f"Completed sale: {len(cart)} item(s), total ₦{total_amount.get():,.2f}")

        messagebox.showinfo("✅ Sale Complete", f"Total: ₦{total_amount.get():,.2f}\nItems sold: {len(cart)}")
        window.destroy()

    window = tk.Toplevel()
    window.title("🛒 ONYXCARE Sales")
    window.geometry("550x700")
    window.configure(bg="white")

    selected_pid = tk.StringVar()
    selected_name = tk.StringVar()
    selected_price = tk.StringVar(value="0")

    tk.Label(window, text="Search Product:", bg="white").pack(pady=5)
    entry_search = tk.Entry(window, width=30)
    entry_search.pack()
    entry_search.bind("<Return>", lambda e: search_product())
    tk.Button(window, text="Search", command=search_product).pack(pady=5)

    listbox_results = tk.Listbox(window, height=6, width=60)
    listbox_results.pack()
    listbox_results.bind("<<ListboxSelect>>", select_product)

    label_price = tk.Label(window, text="Unit Price: ₦0", font=("Arial", 11), bg="white")
    label_price.pack(pady=5)

    tk.Label(window, text="Quantity:", bg="white").pack()
    entry_qty = tk.Entry(window, width=10)
    entry_qty.pack()
    entry_qty.bind("<KeyRelease>", update_live_subtotal)
    entry_qty.bind("<Return>", lambda e: add_to_cart())
    tk.Label(window, textvariable=live_subtotal, bg="white", fg="#2C3E50").pack()

    tk.Button(window, text="Add to Cart", command=add_to_cart, bg="#3498DB", fg="white").pack(pady=8)

    tk.Label(window, text="🧾 Cart:", font=("Arial", 12, "bold"), bg="white").pack()

    cart_table = ttk.Treeview(window, columns=("Product", "Qty", "Price", "Subtotal"), show="headings", height=8)
    cart_table.heading("Product", text="Product")
    cart_table.heading("Qty", text="Qty")
    cart_table.heading("Price", text="Unit Price")
    cart_table.heading("Subtotal", text="Subtotal")
    cart_table.column("Product", width=170)
    cart_table.column("Qty", width=40, anchor="center")
    cart_table.column("Price", width=90, anchor="e")
    cart_table.column("Subtotal", width=100, anchor="e")
    cart_table.pack(pady=5)

    ttk.Button(window, text="✏️ Edit Quantity", command=edit_cart_item).pack(pady=4)
    ttk.Button(window, text="❌ Remove Item", command=remove_cart_item).pack(pady=2)

    label_total = tk.Label(window, text="Total: ₦0", font=("Arial", 13, "bold"), bg="white")
    label_total.pack(pady=10)

    tk.Button(window, text="✅ Checkout", command=checkout, bg="#27AE60", fg="white", font=("Arial", 12)).pack(pady=10)

    add_footer(window)  # ✅ Append footer to the bottom
