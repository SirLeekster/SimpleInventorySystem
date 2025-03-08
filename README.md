# SimpleInventorySystem

### `requirements.txt`
- List of Python dependencies for the app.

### `app.py`
- Main entry point for the Flask app.

### `config.py`
- App configuration (e.g., database connection details, app-wide settings).

---

### `backend/`
Contains all the backend files for the Flask application.

- **`database/`**: Database-related files.
  - `__init__.py`: Initializes the database module for easy import.
  - `database.py`: Contains database methods for connecting and interacting with the database.
  - `dev_database.sql`: SQL script to set up the development database.

- **`models/`**: Data models for representing database entities/tables.
  - `user.py`: Defines the User model.

- **`routes/`**: Flask routes (controllers, API endpoints).
  - `main_routes.py`: Main routes for showing the user interface views.
  - `api_routes.py`: API routes for CRUD operations and authentication.

- **`services/`**: Contains business logic and services.
  - `user_service.py`: Service layer for user-related logic.

---

### `frontend/`
Contains all the frontend files for the application.

- **`static/`**: Static assets like images, CSS, and JS.
  - **`css/`**: CSS stylesheets.
    - `styles.css`: Main CSS file for the frontend.
  - **`js/`**: JavaScript files.
    - `user_actions.js`: Handles user interactions on the frontend.

- **`templates/`**: HTML templates.
  - `home.html`: Main homepage template.
