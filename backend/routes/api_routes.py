from flask import Blueprint, request, jsonify
from backend.services import user_service

from backend.models.user import User

# Create a Blueprint for the main routes
api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.get_json()  # Get the JSON data from the request
    if data:
        new_user = user_service.register(data)
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "Invalid data"}), 400
