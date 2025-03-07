from flask import Blueprint, render_template

# Create a Blueprint for the main routes, with template folder specified
main_routes = Blueprint('main_routes', __name__)

# Home route (home page)
@main_routes.route('/')
def home():
    # Render the home page template
    return render_template('home.html')

