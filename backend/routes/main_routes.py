from flask import Blueprint, render_template, session, redirect, url_for

# Create a Blueprint for the main routes, with the template folder specified
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return redirect(url_for('main_routes.dashboard'))

@main_routes.route('/registration')
def register():
    # Render the registration template
    return render_template('registration.html')

@main_routes.route('/login')
def login():
    # Render the login template
    return render_template('login.html')

@main_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_routes.login'))

@main_routes.route('/dashboard')
def dashboard():
    # Only allow access if the user is logged in (i.e., 'user_id' is in the session)
    if 'user_id' not in session:
        return redirect(url_for('main_routes.login'))
    return render_template('dashboard.html')
