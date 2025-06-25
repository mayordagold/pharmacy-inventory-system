import tkinter as tk
from tkinter import messagebox
import sqlite3
import app
from gui_utils import add_footer  # ✅ Reusable footer

def show_create_user_window():
    win = tk.Toplevel()
    win.title("👤 Create Sales User")
    win.geometry("350x200")
    win.configure(bg="white")

    tk.Label(win, text="Username:", bg="white").pack(pady=5)
    entry_user = tk.Entry(win, font=("Arial", 12))
    entry_user.pack()

    tk.Label(win, text="Password:", bg="white").pack(pady=5)
    entry_pass = tk.Entry(win, show="*", font=("Arial", 12))
    entry_pass.pack()

    def submit():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("⚠️ Missing Info", "Please fill in all fields.")
            return
        try:
            conn = sqlite3.connect(app.db_path)
            cursor = conn.cursor()
            hashed_pw = app.hash_password(password)
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, "sales_user"))
            conn.commit()
            conn.close()
            messagebox.showinfo("✅ Success", f"Sales user '{username}' created.")
            win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("❌ Error", "Username already exists.")

    tk.Button(win, text="Create User", command=submit, bg="#2ECC71", fg="white").pack(pady=15)

    add_footer(win)  # ✅ Add footer at the bottom