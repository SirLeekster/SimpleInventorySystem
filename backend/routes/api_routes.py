from flask import Blueprint, request, jsonify
from backend.services import user_service, inventory_service

# Create a Blueprint
api_routes = Blueprint('api_routes', __name__)

# --- USER ROUTES ---

@api_routes.route('/api/create_user', methods=['POST'])
def create_user():
    user_data:dict = request.get_json()
    if user_data:
        success:bool = user_service.add_user_to_db(user_data)
        if success:
            return jsonify({"message": f"User created successfully"}), 201
    return jsonify({"message": "Invalid data"}), 400


# --- INVENTORY ROUTES ---
@api_routes.route('/api/get_all_inventory_items', methods=['GET'])
def get_all_inventory_items():
    inventory_items:list[dict] = inventory_service.get_inventory_from_db()
    if inventory_items:
        return jsonify(inventory_items), 200
    return jsonify({"message": "No inventory items found"}), 404

@api_routes.route('/api/create_inventory_item', methods=['POST'])
def create_inventory_item():
    item:dict = request.get_json()
    if item:
        success:bool = inventory_service.add_inventory_item_to_db(item)
        if success:
            return jsonify({
                "message": "Inventory item created successfully",
                "item_id": item.id
            }), 201
    return jsonify({"message": "Invalid data"}), 400
