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
  - `database.py`: Handles DB connection.
  - `dev_database.sql`: SQL script for development DB schema.

- **`models/`** – ORM models (SQLAlchemy):
  - `user.py`: User table.
  - `organization.py`: Organization table.
  - `inventory_item.py`: Inventory item schema.
  - `inventory_sku.py`: SKU table (individual units).

- **`routes/`** – Flask route handlers:
  - `main_routes.py`: Serves HTML templates.
  - `api_routes.py`: API endpoints for inventory, users, auth, SKUs, etc.

- **`services/`** – Core business logic:
  - `user_service.py`: User account operations.
  - `organization_service.py`: Org-level functionality.
  - `inventory_service.py`: Inventory & SKU logic and helpers.

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
