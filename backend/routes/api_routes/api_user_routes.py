from flask import Blueprint, request, jsonify, session
from backend.services import user_service
from backend.models.user import User

api_user_routes = Blueprint('api_user_routes', __name__)


# ======================
# USER ROUTES
# ======================

# create a new user
@api_user_routes.route('/api/create_user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    print("Received user data:", user_data)
    if not user_data:
        return jsonify({"message": "No JSON received"}), 400

    new_user = user_service.add_user_to_db(user_data)
    if new_user and isinstance(new_user, User):
        return jsonify({"message": "User created successfully"}), 201
    elif new_user == "duplicate":
        return jsonify({"message": "Email already exists"}), 409
    elif new_user == "organization_not_found":
        return jsonify({"message": "Organization not found"}), 404
    else:
        return jsonify({"message": "Failed to create user"}), 400


# log in a user
@api_user_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_service.login_user(data)
    if user:
        session['user_id'] = user.user_id
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


# placeholder for forgot password functionality
@api_user_routes.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    # need to implement real password reset/email system
    return jsonify({"message": f"Reset instructions sent to {email}"}), 200
