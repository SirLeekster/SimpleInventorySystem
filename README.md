SimpleInventorySystem
├── requirements.txt              # List of Python dependencies for the app
├── app.py                        # Main Flask app entry point
├── config.py                     # App configuration (e.g., database info, etc)

├── backend/                      # All backend files (Flask routes, models, services, security, etc)
│   ├── database/                 # Database-related files 
│   │   ├── __init__.py           # Initializes the database module, making it easier to import
│   │   ├── database.py           # Handles database methods
│   │   ├── dev_database.sql      # SQL file to initialize the development database
│   ├── models/                   # Data models (database entities/tables)
│   │   └── user.py               # User model, representing user data in the database
│   ├── routes/                   # Flask routes (controllers, API endpoints)
│   │   ├── main_routes.py        # Main application routes (show the user interface views)
│   │   ├── api_routes.py         # API endpoints (to call CRUD operations, authentication, etc)
│   ├── services/                 # Business logic, CRUD operations, and services
│   │   └── user_service.py       # Service layer for user-related business logic

├── frontend/                     # All frontend files (HTML, CSS, JS)
│   ├── static/                   # Static assets (images, CSS, JS)
│   │   ├── css/                  # CSS stylesheets
│   │   │   └── styles.css        # Main CSS file for styling the frontend
│   │   ├── js/                   # JavaScript files for frontend functionality
│   │   │   └── user_actions.js   # JavaScript file handling user interactions
│   ├── templates/                # HTML templates (frontend pages)
│   │   └── home.html             # Main HTML page for the application (homepage)
