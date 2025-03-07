from flask import Flask
from backend.routes.main_routes import main_routes
from backend.routes.api_routes import api_routes
from backend.database import db
from config import Config
import os

# Create the Flask app instance
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Set the static and template folder paths after initializing the app
app.static_folder = os.path.join(app.root_path, 'frontend/static')
app.template_folder = os.path.join(app.root_path, 'frontend/templates')

# Register Blueprints for routing
app.register_blueprint(main_routes)
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(debug=True)
