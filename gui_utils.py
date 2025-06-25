import tkinter as tk

def add_footer(parent):
    footer = tk.Label(
        parent,
        text="© 2025 Olumayowa A. | Licensed under the MIT License",
        font=("Arial", 9),
        fg="gray",
        bg=parent["bg"]
    )
    footer.pack(side="bottom", pady=5)