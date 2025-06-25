import tkinter as tk
from tkinter import messagebox
import sqlite3
import app  # For db_path, hash_password, and log_user_action
from gui_utils import add_footer  # ✅ Reusable footer

def show_create_admin_user_window(current_admin):
    win = tk.Toplevel()
    win.title("👑 Create Admin User")
    win.geometry("380x280")
    win.configure(bg="white")

    tk.Label(win, text="👑 Create New Admin", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(pady=15)

    tk.Label(win, text="Username:", bg="white", anchor="w").pack(fill="x", padx=30)
    entry_username = tk.Entry(win, font=("Arial", 12))
    entry_username.pack(padx=30, pady=5, fill="x")

    tk.Label(win, text="Password:", bg="white", anchor="w").pack(fill="x", padx=30)
    entry_password = tk.Entry(win, font=("Arial", 12), show="*")
    entry_password.pack(padx=30, pady=5, fill="x")

    def create_admin_user():
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return

        hashed_pw = app.hash_password(password)
        try:
            conn = sqlite3.connect(app.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')", (username, hashed_pw))
            conn.commit()
            conn.close()

            app.log_user_action(current_admin, f"Created new admin user: {username}")
            messagebox.showinfo("✅ Success", f"Admin user '{username}' created successfully.")
            win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("❌ Error", "Username already exists.")

    tk.Button(win, text="✅ Create Admin", command=create_admin_user, bg="#3498DB", fg="white", font=("Arial", 11), width=20).pack(pady=20)

    add_footer(win)  # ✅ Add footer at the bottom