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
