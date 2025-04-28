from flask import Blueprint, render_template, session, redirect, url_for

# create a blueprint for the main routes, with the template folder specified
main_routes = Blueprint('main_routes', __name__)


# route for the homepage, redirects to dashboard
@main_routes.route('/')
def index():
    return redirect(url_for('main_routes.dashboard'))


# route for the registration page
@main_routes.route('/registration')
def register():
    # render the registration template
    return render_template('registration.html')


# route for the login page
@main_routes.route('/login')
def login():
    # render the login template
    return render_template('login.html')


# route for logging out
@main_routes.route('/logout')
def logout():
    # clear session and redirect to login
    session.clear()
    return redirect(url_for('main_routes.login'))


# route for the dashboard page
@main_routes.route('/dashboard')
def dashboard():
    # only allow access if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('main_routes.login'))
    # render the dashboard template
    return render_template('dashboard.html')
