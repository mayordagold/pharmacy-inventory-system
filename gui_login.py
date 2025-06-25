import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from PIL import Image, ImageTk
from tkinter import ttk
from gui_dashboard import launch_dashboard
import app  # ✅ Import app to use log_user_action
from gui_utils import add_footer  # ✅ Import reusable footer

db_path = "C:/Users/USER/OneDrive/Desktop/chemist-inventory/inventory.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def attempt_login(username_entry, password_entry, login_window):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Missing Info", "Please enter both username and password.")
        return

    hashed = hash_password(password)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed))
        result = cursor.fetchone()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")
        return

    if result:
        role = result[0]
        app.log_user_action(username, "Logged in")  # ✅ Log the login action
        login_window.destroy()
        launch_dashboard(username, role)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def show_login():
    login_window = tk.Tk()
    login_window.title("💊 ONYXCARE Login")
    login_window.geometry("440x540")
    login_window.resizable(False, False)
    login_window.configure(bg="#EAF2F8")

    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Arial", 12, "bold"),
        background="#1ABC9C",
        foreground="white",
        padding=10,
        borderwidth=0
    )
    style.map(
        "TButton",
        background=[("active", "#17A589"), ("pressed", "#148F77")],
        relief=[("pressed", "groove"), ("!pressed", "flat")]
    )

    # Content frame
    frame = tk.Frame(login_window, bg="white", bd=0, relief="flat", padx=30, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="ONYXCARE", font=("Helvetica", 22, "bold"), fg="#2C3E50", bg="white").pack(pady=(10, 5))
    tk.Label(frame, text="Inventory made simple. Health made smart.", font=("Helvetica", 9), fg="#7F8C8D", bg="white").pack()

    try:
        img = Image.open("onyxcare_logo.png")
        img = img.resize((90, 90), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img)
        tk.Label(frame, image=logo, bg="white").pack(pady=5)
        frame.logo_img = logo
    except:
        pass

    tk.Label(frame, text="Username", font=("Arial", 11), bg="white", anchor="w").pack(fill="x", pady=(20, 0))
    username_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=1, relief="solid", highlightthickness=1, highlightcolor="#BDC3C7")
    username_entry.pack(pady=5)

    tk.Label(frame, text="Password", font=("Arial", 11), bg="white", anchor="w").pack(fill="x", pady=(10, 0))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30, bd=1, relief="solid", highlightthickness=1, highlightcolor="#BDC3C7")
    password_entry.pack(pady=5)

    ttk.Button(
        frame,
        text="🔐 Sign In",
        command=lambda: attempt_login(username_entry, password_entry, login_window)
    ).pack(pady=30)

    # ✅ Add footer to login window
    add_footer(login_window)

    login_window.mainloop()