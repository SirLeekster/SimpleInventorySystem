from flask import Flask
from backend.routes.main_routes import main_routes
from backend.routes.api_routes.api_dashboard_routes import api_dashboard_routes
from backend.routes.api_routes.api_inventory_routes import api_inventory_routes
from backend.routes.api_routes.api_sales_routes import api_sales_routes
from backend.routes.api_routes.api_settings_routes import api_settings_routes
from backend.routes.api_routes.api_user_routes import api_user_routes
from backend.routes.api_routes.api_suppliers_orders_routes import api_suppliers_orders_routes
from backend.database import db
from config import Config
import os

# create the Flask app instance
app = Flask(__name__)

# load configuration from config.py
app.config.from_object(Config)

# make sure the secret key is set for session management
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = os.urandom(24)  # backup if SECRET_KEY not in Config

# initialize the database
db.init_app(app)

# set the static and template folder paths after initializing the app
app.static_folder = os.path.join(app.root_path, 'frontend/static')
app.template_folder = os.path.join(app.root_path, 'frontend/templates')

# register blueprints for routing
app.register_blueprint(main_routes)
app.register_blueprint(api_dashboard_routes)
app.register_blueprint(api_inventory_routes)
app.register_blueprint(api_sales_routes)
app.register_blueprint(api_settings_routes)
app.register_blueprint(api_user_routes)
app.register_blueprint(api_suppliers_orders_routes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

