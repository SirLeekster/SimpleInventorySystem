from flask import Blueprint, request, jsonify, session
from backend.services import user_service, inventory_service, log_service
from backend.models.inventory_item import Inventory_Item
from backend.models.inventory_sku import InventorySKU
from backend.models.sale import Sale
from backend.database import db
import requests
import traceback

api_inventory_routes = Blueprint('api_inventory_routes', __name__)


# ========================
# INVENTORY ROUTES
# ========================

# upc lookup using external api
@api_inventory_routes.route('/api/upc_lookup', methods=['GET'])
def upc_lookup():
    upc = request.args.get('upc')
    if not upc:
        return jsonify({"message": "UPC is required"}), 400

    try:
        response = requests.get(
            f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}",
            proxies={"http": None, "https": None}
        )
        data = response.json()
        if response.status_code != 200 or not data.get("items"):
            return jsonify({"message": "No data found for that UPC"}), 404

        item = data["items"][0]
        return jsonify({
            "product_name": item.get("title", ""),
            "description": item.get("description", ""),
            "category": item.get("category", ""),
            "price": item.get("lowest_recorded_price", "")
        }), 200

    except Exception as e:
        return jsonify({"message": f"Error during UPC lookup: {str(e)}"}), 500


# create a new inventory item
@api_inventory_routes.route('/api/create_inventory_item', methods=['POST'])
def create_inventory_item():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    item_data = request.get_json()
    if not item_data:
        return jsonify({"message": "Invalid or missing JSON"}), 400
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403
    result = inventory_service.add_inventory_item_to_db(item_data, user)
    if result and isinstance(result, Inventory_Item):
        log_service.log_user_action(user.user_id, f"Created item ID {result.id} - {result.product_name}")
        return jsonify({"message": "Inventory item created successfully", "item_id": result.id}), 201
    return jsonify({"message": "Failed to create inventory item"}), 400


# upload an image for an inventory item
@api_inventory_routes.route('/api/upload_inventory_image/<int:item_id>', methods=['POST'])
def upload_inventory_image(item_id):
    if 'user_id' not in session or 'image' not in request.files:
        return jsonify({"message": "Not authenticated or missing image"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403
    image = request.files['image']
    from backend.services.inventory_service import save_inventory_image
    success, result = save_inventory_image(item_id, image)
    if success:
        log_service.log_user_action(user.user_id, f"Uploaded image for item ID {item_id}")
        return jsonify({"message": "Image uploaded successfully", "image_path": result}), 200
    return jsonify({"message": result}), 400


# update quantity of an inventory item
@api_inventory_routes.route('/api/update_inventory_quantity/<int:item_id>', methods=['PUT'])
def update_inventory_quantity(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403
    data = request.get_json()
    if not data or 'change' not in data:
        return jsonify({"message": "Missing 'change' in request body"}), 400
    try:
        updated_item = inventory_service.update_item_quantity(item_id, data['change'])
        log_service.log_user_action(user.user_id, f"Updated quantity of item ID {item_id} to {updated_item.quantity}")
        return jsonify({
            "message": "Item quantity updated successfully",
            "item_id": updated_item.item_id,
            "new_quantity": updated_item.quantity
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# fetch all inventory items for the logged in user's organization
@api_inventory_routes.route('/api/inventory_items', methods=['GET'])
def get_inventory_items():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    items = inventory_service.get_items_for_org(user.organization_id)
    data = [{
        "id": item.id,
        "product_name": item.product_name,
        "description": item.description,
        "category": item.category,
        "quantity": item.quantity,
        "price": str(item.price),
        "image_path": item.image_path or ""
    } for item in items]
    return jsonify(data), 200


# update fields of an inventory item
@api_inventory_routes.route('/api/update_inventory_item/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid or missing JSON"}), 400
    item = Inventory_Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    item.product_name = data.get("product_name", item.product_name)
    item.description = data.get("description", item.description)
    item.category = data.get("category", item.category)
    item.quantity = data.get("quantity", item.quantity)
    item.price = data.get("price", item.price)
    try:
        db.session.commit()
        log_service.log_user_action(user.user_id, f"Edited item ID {item_id} - {item.product_name}")
        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to update item: {str(e)}"}), 500


# delete an inventory item
@api_inventory_routes.route('/api/delete_inventory_item/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin']):
        return jsonify({"message": "Access denied"}), 403
    item = Inventory_Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404
    try:
        db.session.delete(item)
        db.session.commit()
        log_service.log_user_action(user.user_id, f"Deleted item ID {item_id} - {item.product_name}")
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to delete item: {str(e)}"}), 500


# add a new sku to an inventory item
@api_inventory_routes.route('/api/add_sku_to_inventory_item/<int:item_id>', methods=['POST'])
def add_sku_to_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    if not data or 'sku_code' not in data:
        return jsonify({"message": "Missing required SKU code"}), 400

    new_sku = InventorySKU(
        inventory_id=item_id,
        sku_code=data['sku_code'],
        serial_number=data.get('serial_number'),
        status=data.get('status', 'in_stock'),
        expiration_date=data.get('expiration_date')
    )

    try:
        db.session.add(new_sku)
        db.session.commit()
        log_service.log_user_action(user.user_id, f"Added SKU {new_sku.sku_code} to item ID {item_id}")
        return jsonify({"message": "SKU added successfully", "sku_id": new_sku.sku_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to add SKU: {str(e)}"}), 500


# fetch all skus for an inventory item
@api_inventory_routes.route('/api/inventory_item_skus/<int:item_id>', methods=['GET'])
def fetch_skus_for_item(item_id):
    try:
        skus = InventorySKU.query.filter_by(inventory_id=item_id).all()
        data = [{
            "sku_id": sku.sku_id,
            "sku_code": sku.sku_code,
            "serial_number": sku.serial_number,
            "status": sku.status,
            "expiration_date": sku.expiration_date.isoformat() if sku.expiration_date else None
        } for sku in skus]
        return jsonify(data), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': 'Error fetching SKUs', 'error': str(e)}), 500


# update fields of a specific sku
@api_inventory_routes.route('/api/update_sku/<int:sku_id>', methods=['PATCH'])
def update_sku(sku_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403

    sku = InventorySKU.query.get(sku_id)
    if not sku:
        return jsonify({"message": "SKU not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing JSON data"}), 400

    original_status = sku.status
    new_status = data.get("status", sku.status)
    sku.sku_code = data.get("sku_code", sku.sku_code)
    sku.serial_number = data.get("serial_number", sku.serial_number)
    sku.status = new_status
    sku.expiration_date = data.get("expiration_date", sku.expiration_date)

    item = Inventory_Item.query.get(sku.inventory_id)
    if not item:
        return jsonify({"message": "Item not found for SKU"}), 404

    if original_status != "sold" and new_status == "sold":
        db.session.add(Sale(
            inventory_id=item.id,
            sku_id=sku.sku_id,
            organization_id=item.organization_id,
            price=item.price
        ))
    if original_status == "sold" and new_status != "sold":
        Sale.query.filter_by(sku_id=sku.sku_id).delete()
    if original_status == "in_stock" and new_status in ["sold", "damaged"]:
        if item.quantity <= 0:
            return jsonify({"message": "Cannot reduce quantity below 0"}), 400
        item.quantity -= 1
    if original_status in ["sold", "damaged"] and new_status == "in_stock":
        item.quantity += 1

    try:
        db.session.commit()
        log_service.log_user_action(user.user_id, f"Edited SKU ID {sku_id} - {sku.sku_code}")
        return jsonify({"message": "SKU updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to update SKU or log sale: {str(e)}"}), 500


# delete a sku
@api_inventory_routes.route('/api/delete_sku/<int:sku_id>', methods=['DELETE'])
def delete_sku(sku_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin']):
        return jsonify({"message": "Access denied"}), 403

    sku = InventorySKU.query.get(sku_id)
    if not sku:
        return jsonify({"message": "SKU not found"}), 404

    try:
        db.session.delete(sku)
        db.session.commit()
        log_service.log_user_action(user.user_id, f"Deleted SKU ID {sku_id} - {sku.sku_code}")
        return jsonify({"message": "SKU deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to delete SKU: {str(e)}"}), 500


# auto-generate missing skus for an inventory item
@api_inventory_routes.route('/api/generate_skus/<int:item_id>', methods=['POST'])
def generate_skus(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    if not user_service.user_has_role(user.user_id, ['admin']):
        return jsonify({"message": "Access denied"}), 403

    try:
        item = Inventory_Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        desired_count = item.quantity
        current_count = InventorySKU.query.filter_by(inventory_id=item_id).count()
        missing_count = desired_count - current_count

        if missing_count <= 0:
            return jsonify({"message": "No new SKUs needed. Already at or above quantity."}), 200

        for i in range(current_count + 1, desired_count + 1):
            sku = InventorySKU(
                inventory_id=item_id,
                sku_code=f"AUTO-SKU-{item_id}-{i}",
                status="in_stock"
            )
            db.session.add(sku)

        db.session.commit()
        log_service.log_user_action(user.user_id, f"Auto-generated {missing_count} SKUs for item ID {item_id}")
        return jsonify({"message": f"{missing_count} new SKUs generated."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to generate SKUs: {str(e)}"}), 500
