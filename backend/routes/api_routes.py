from flask import Blueprint, request, jsonify, session
from backend.services import user_service, inventory_service
from backend.models.user import User

api_routes = Blueprint('api_routes', __name__)

# ========================
# USER ROUTES
# ========================

@api_routes.route('/api/create_user', methods=['POST'])
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

@api_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON received"}), 400

    user = user_service.login_user(data)
    if user:
        session['user_id'] = user.user_id
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


# ========================
# INVENTORY ROUTES
# ========================

@api_routes.route('/api/create_inventory_item', methods=['POST'])
def create_inventory_item():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    item_data = request.get_json()
    if not item_data:
        return jsonify({"message": "Invalid or missing JSON"}), 400

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    result = inventory_service.add_inventory_item_to_db(item_data, user)
    if result:
        return jsonify({"message": "Inventory item created successfully"}), 201

    return jsonify({"message": "Failed to create inventory item"}), 400

# ========================
# ROUTES FOR API
# ========================
@api_routes.route('/api/update_inventory_quantity/<int:item_id>', methods=['PUT'])
def update_inventory_quantity(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    data = request.get_json()
    if not data or 'change' not in data:
        return jsonify({"message": "Missing 'change' in request body"}), 400

    change = data['change']

    try:
        updated_item = inventory_service.update_item_quantity(item_id, change)
        return jsonify({
            "message": "Item quantity updated successfully",
            "item_id": updated_item.item_id,
            "new_quantity": updated_item.quantity
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ========================
# DASHBOARD ROUTES
# ========================
@api_routes.route('/api/dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    from backend.services import inventory_service, user_service

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    org_id = user.organization_id
    stats = inventory_service.get_dashboard_stats_for_org(org_id)

    return jsonify(stats), 200
