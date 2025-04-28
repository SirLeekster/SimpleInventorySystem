# SimpleInventorySystem

### `requirements.txt`
- List of Python dependencies for the app.

### `app.py`
- Main entry point for the Flask app.

### `config.py`
- App configuration (e.g., database connection details, app-wide settings).

### `README.md`
- Project overview and instructions.

---

### `backend/`
Contains all backend logic and structure for the Flask server.

- **`database/`** – Database-related files:
  - `__init__.py`: Initializes the database package.
  - `dev_database.sql`: SQL script for development DB schema.

- **`models/`** – ORM models (SQLAlchemy):
  - `user.py`: User table.
  - `organization.py`: Organization table.
  - `inventory_item.py`: Inventory item schema.
  - `inventory_sku.py`: SKU table (individual units).
  - `inventory_order.py`: Tracks supplier inventory orders.
  - `user_log.py`: Logs user actions (e.g., login, edits).
  - `sale.py`: Sales records for inventory items.
  - `supplier.py`: Supplier details for inventory sourcing.

- **`routes/`** – Flask route handlers:
  - `main_routes.py`: Serves HTML templates.
  - **`api_routes/`**:
    - `api_dashboard_routes.py`: Dashboard overview data.
    - `api_inventory_routes.py`: CRUD for inventory items and SKUs.
    - `api_sales_routes.py`: API for sales and purchase records.
    - `api_settings_routes.py`: Handles user settings updates.
    - `api_suppliers_orders_routes.py`: Supplier and order operations.
    - `api_user_routes.py`: Registration, login, user management.

- **`services/`** – Core business logic:
  - `user_service.py`: User account operations.
  - `organization_service.py`: Org-level functionality.
  - `inventory_service.py`: Inventory & SKU logic and helpers.
  - `inventory_order_service.py`: Handles supplier order processing.
  - `log_service.py`: Handles recording and retrieving user logs.
  - `report_service.py`: Compiles reports and analytics.
  - `supplier_service.py`: Handles suppliers and inventory ordering.

---

### `frontend/`
Frontend templates and assets served via Flask.

- **`static/`** – Static files:
  - **`css/`**
    - `base.css`: Shared layout/base styles.
    - `dashboard.css`: Full dashboard UI styling.
    - `login.css`: Login form layout.
    - `registration.css`: Registration page styles.
  - **`js/`**
    - `login.js`: JS logic for login form.
    - `registration.js`: Handles frontend registration.
    - **`dashboard/`**
      - `dashboard.js`: Entry point, handles routing between sections.
      - `dashboard-overview.js`: Dashboard overview data/stats.
      - `dashboard-add-item.js`: Form handling for adding inventory.
      - `dashboard-manage-items.js`: Logic for managing inventory items and SKUs.
      - `dashboard-reports.js`: Placeholder for sales/analytics.
      - `dashboard-settings.js`: User profile + password update.
  - **`image_uploads/`**
    - Product images uploaded by user (e.g., `Laptop.jpg`, `PS5.jpg`).

- **`templates/`** – Jinja HTML templates:
  - `dashboard.html`: Main user dashboard view.
  - `login.html`: Login screen layout.
  - `registration.html`: User sign-up template.




## Self-Hosting Guide

### Requirements

- Python 3.10 or newer
- MySQL 8.0+ Server
- Git
- Linux, WSL, or Windows (any environment that can run Python and MySQL)

---






## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SirLeekster/SimpleInventorySystem.git
   cd SimpleInventorySystem
   ```

2. **Host a MySQL Server**

   Install and start a MySQL server locally or on a remote machine.  
   [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)

3. **Import the Database**

   Use the provided SQL file to set up the database.  
   This will automatically create the database, tables, and indexes.

   ```bash
   mysql -u your-username -p < backend/database/dev_database.sql
   ```

4. **Install Python and Python Dependencies**

   If you do not already have Python installed, download and install it first:  
   [Python Downloads (Windows, Mac, Linux)](https://www.python.org/downloads/)

   Make sure to check "**Add Python to PATH**" during installation on Windows.

   Then install project dependencies:

   On **Linux or Mac**:

   ```bash
   pip install -r requirements.txt
   ```

   On **Windows** (recommended if `pip` is not recognized):

   ```bash
   python -m pip install -r requirements.txt
   ```

   > ⚠️ **Tip for Windows Users:**  
   > If `pip` is not recognized, use `python -m pip` instead.  
   > If pip is missing, you can install it by running:
   > ```bash
   > python -m ensurepip --upgrade
   > ```

5. **Configure the Application**

   Open `config.py` and update the database settings inside the `Config` class:

   ```python
   class Config:
       # database settings
       DB_HOST = 'your-mysql-host'
       DB_USER = 'your-mysql-username'
       DB_PASSWORD = 'your-mysql-password'
       DB_NAME = 'simpleinventorysystem'
   ```

   > ⚠️ **Important:** `config.py` contains sensitive information (database login).  
   > Update these values before running the application.

6. **Run the Application**

   On **Linux or Mac**:

   ```bash
   python3 -m flask run
   ```

   On **Windows**:

   ```bash
   python -m flask run
   ```

   The app will start on `http://localhost:5000`.

---

## ⚠️ Security Warnings

- **Database credentials** are hardcoded in `config.py`.
- **Session management** uses Flask defaults; no custom session hardening is implemented.
- **API is open** — there is no authentication or API key required.
- **Forgot password feature** exists in the UI but has **no backend functionality**.
- **No HTTPS** — the app does not natively handle HTTPS. Use a reverse proxy like NGINX if needed.
