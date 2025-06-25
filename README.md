# 💊 Pharmacy Inventory System (Offline Desktop App)

Originally developed for ONYXCARE Pharmacy, this desktop application is a secure and efficient solution for managing pharmaceutical, Stores, and supermarket inventory and sales without needing an internet connection.

---

## 🌟 Features

- **Role-based Login**: Admin and Sales User access with secure authentication
- **Inventory Control**: Add, restock, and view stock levels with expiry tracking
- **Sales Recording**: Smart cart interface with automatic stock deductions
- **Analytics Dashboard**: View top-selling products, low stock alerts, and monthly trends
- **Activity Logs**: Admins can review who did what, and when
- **Offline-First**: Runs 100% on desktop, using SQLite under the hood

---

## 🛠 Built With

- Python (3.9+)
- Tkinter (GUI)
- SQLite3 (Local Database)
- Matplotlib (Charts & Analytics)
- PIL (Logo and image loading)

---

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your-username/pharmacy-inventory-system.git
cd pharmacy-inventory-system

2. Run the login screen:
python gui_login.py    #Make sure your Python environment includes required libraries: matplotlib, Pillow

3. Default Credentials:
Username: admin_user
password: admin123

## Folder structure:

pharmacy-inventory-system/
│
├── gui_login.py
├── gui_dashboard.py
├── gui_add_product.py
├── gui_record_sale.py
├── gui_restock_product.py
├── gui_transaction_history.py
├── gui_search_product.py
├── gui_inventory_table.py
├── gui_analytics.py
├── gui_view_logs.py
├── gui_utils.py
├── app.py
├── inventory.db
├── README.md
└── LICENSE

📜 License
This project is released under the MIT License. See LICENSE for details.
© 2025 Olumayowa A. — Designed with real-world use in mind.



