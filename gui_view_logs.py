import tkinter as tk
from tkinter import ttk
import sqlite3
import app
from gui_utils import add_footer  # ✅ Import reusable footer

def show_activity_log_window():
    window = tk.Toplevel()
    window.title("📜 User Activity Log")
    window.geometry("650x500")
    window.configure(bg="white")

    tk.Label(window, text="User Activity Logs", font=("Arial", 16, "bold"), bg="white", fg="#2C3E50").pack(pady=10)

    tree = ttk.Treeview(window, columns=("Username", "Action", "Timestamp"), show="headings", height=20)
    tree.heading("Username", text="Username")
    tree.heading("Action", text="Action Performed")
    tree.heading("Timestamp", text="Timestamp")

    tree.column("Username", width=120, anchor="center")
    tree.column("Action", width=340, anchor="w")
    tree.column("Timestamp", width=170, anchor="center")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Load data from database
    conn = sqlite3.connect(app.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT username, action, timestamp FROM activity_logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()

    for row in logs:
        tree.insert("", "end", values=row)

    add_footer(window)  # ✅ Add footer at the bottom